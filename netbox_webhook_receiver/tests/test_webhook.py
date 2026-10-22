import hashlib
import hmac
import json
import uuid
from unittest import mock

from django.test import TestCase, override_settings
from django.urls import reverse

from core.choices import JobStatusChoices
from core.jobs import SyncDataSourceJob
from core.models import DataSource, Job
from netbox_webhook_receiver.choices import (
    HashingAlgorithmChoices,
    WebhookAuthMethodChoices,
)
from netbox_webhook_receiver.models import WebhookMessage, WebhookReceiver

PAYLOAD = json.dumps({"ref": "refs/heads/main"}).encode()


def sign(secret, body, algorithm):
    return hmac.new(secret.encode(), body, getattr(hashlib, algorithm)).hexdigest()


class IncomingWebhookTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.datasource = DataSource.objects.create(
            name="Data Source 1", type="local", source_url="file:///tmp/"
        )
        cls.token_receiver = WebhookReceiver.objects.create(
            name="Token Receiver",
            auth_method=WebhookAuthMethodChoices.TOKEN,
            auth_header="X-Gitlab-Token",
            token="gitlab-token",
            store_payload=False,
        )
        cls.signature_receiver = WebhookReceiver.objects.create(
            name="Signature Receiver",
            auth_method=WebhookAuthMethodChoices.SIGNATURE_VERIFICATION,
            auth_header="X-Hub-Signature-256",
            secret_key="github-secret",
            hash_algorithm=HashingAlgorithmChoices.SHA_256,
            store_payload=False,
        )

    def post(self, receiver, headers=None, data=PAYLOAD):
        return self.client.post(
            receiver.get_webhook_url(),
            data=data,
            content_type="application/json",
            headers=headers or {},
        )

    def test_webhook_url(self):
        self.assertEqual(
            self.token_receiver.get_webhook_url(),
            f"/plugins/webhook-receiver/webhooks/{self.token_receiver.uuid}/",
        )

    def test_get_not_allowed(self):
        response = self.client.get(self.token_receiver.get_webhook_url())
        self.assertEqual(response.status_code, 405)

    def test_unknown_uuid(self):
        url = reverse("plugins:netbox_webhook_receiver:webhook", args=[uuid.uuid4()])
        response = self.client.post(url, data=PAYLOAD, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_missing_auth_header(self):
        response = self.post(self.token_receiver)
        self.assertEqual(response.status_code, 403)

    def test_token_valid(self):
        response = self.post(
            self.token_receiver, headers={"X-Gitlab-Token": "gitlab-token"}
        )
        self.assertEqual(response.status_code, 200)

    def test_token_invalid(self):
        response = self.post(self.token_receiver, headers={"X-Gitlab-Token": "wrong"})
        self.assertEqual(response.status_code, 403)

    def test_token_ignored_for_signature_method(self):
        # A leftover token must not authenticate a receiver using signatures
        WebhookReceiver.objects.filter(pk=self.signature_receiver.pk).update(
            token="leftover"
        )
        self.signature_receiver.refresh_from_db()
        response = self.post(
            self.signature_receiver, headers={"X-Hub-Signature-256": "leftover"}
        )
        self.assertEqual(response.status_code, 403)

    def test_signature_with_github_prefix(self):
        signature = sign("github-secret", PAYLOAD, "sha256")
        response = self.post(
            self.signature_receiver,
            headers={"X-Hub-Signature-256": f"sha256={signature}"},
        )
        self.assertEqual(response.status_code, 200)

    def test_signature_without_prefix(self):
        signature = sign("github-secret", PAYLOAD, "sha256")
        response = self.post(
            self.signature_receiver, headers={"X-Hub-Signature-256": signature}
        )
        self.assertEqual(response.status_code, 200)

    def test_signature_defaults_to_sha512(self):
        WebhookReceiver.objects.filter(pk=self.signature_receiver.pk).update(
            hash_algorithm=None
        )
        self.signature_receiver.refresh_from_db()
        signature = sign("github-secret", PAYLOAD, "sha512")
        response = self.post(
            self.signature_receiver,
            headers={"X-Hub-Signature-256": f"sha512={signature}"},
        )
        self.assertEqual(response.status_code, 200)

    def test_signature_invalid(self):
        signature = sign("wrong-secret", PAYLOAD, "sha256")
        response = self.post(
            self.signature_receiver,
            headers={"X-Hub-Signature-256": f"sha256={signature}"},
        )
        self.assertEqual(response.status_code, 403)

    def test_store_json_payload(self):
        WebhookReceiver.objects.filter(pk=self.token_receiver.pk).update(
            store_payload=True
        )
        self.token_receiver.refresh_from_db()
        self.post(self.token_receiver, headers={"X-Gitlab-Token": "gitlab-token"})
        message = WebhookMessage.objects.get()
        self.assertEqual(message.receiver, self.token_receiver)
        self.assertEqual(message.payload, {"ref": "refs/heads/main"})

    def test_store_non_json_payload(self):
        WebhookReceiver.objects.filter(pk=self.token_receiver.pk).update(
            store_payload=True
        )
        self.token_receiver.refresh_from_db()
        response = self.post(
            self.token_receiver,
            headers={"X-Gitlab-Token": "gitlab-token"},
            data=b"payload=%7B%7D",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(WebhookMessage.objects.get().payload, "payload=%7B%7D")

    @mock.patch.object(SyncDataSourceJob, "enqueue")
    def test_sync_datasource(self, enqueue):
        WebhookReceiver.objects.filter(pk=self.token_receiver.pk).update(
            datasource=self.datasource
        )
        self.token_receiver.refresh_from_db()
        response = self.post(
            self.token_receiver, headers={"X-Gitlab-Token": "gitlab-token"}
        )
        self.assertEqual(response.status_code, 200)
        enqueue.assert_called_once_with(instance=self.datasource, user=None)

    @mock.patch.object(SyncDataSourceJob, "enqueue")
    def test_sync_datasource_already_queued(self, enqueue):
        WebhookReceiver.objects.filter(pk=self.token_receiver.pk).update(
            datasource=self.datasource
        )
        self.token_receiver.refresh_from_db()
        Job.objects.create(
            name=SyncDataSourceJob.name,
            object=self.datasource,
            status=JobStatusChoices.STATUS_PENDING,
            job_id=uuid.uuid4(),
        )
        response = self.post(
            self.token_receiver, headers={"X-Gitlab-Token": "gitlab-token"}
        )
        self.assertEqual(response.status_code, 200)
        enqueue.assert_not_called()

    @override_settings(
        PLUGINS_CONFIG={
            "netbox_webhook_receiver": {
                "job_user": "missing",
                "payload_retention_days": 2,
            }
        }
    )
    @mock.patch.object(SyncDataSourceJob, "enqueue")
    def test_sync_datasource_unknown_job_user(self, enqueue):
        WebhookReceiver.objects.filter(pk=self.token_receiver.pk).update(
            datasource=self.datasource
        )
        self.token_receiver.refresh_from_db()
        self.post(self.token_receiver, headers={"X-Gitlab-Token": "gitlab-token"})
        enqueue.assert_called_once_with(instance=self.datasource, user=None)
