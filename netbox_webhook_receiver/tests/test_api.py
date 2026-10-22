from django.urls import reverse
from rest_framework import status

from utilities.testing import APITestCase, APIViewTestCases
from netbox_webhook_receiver.choices import (
    HashingAlgorithmChoices,
    WebhookAuthMethodChoices,
)
from netbox_webhook_receiver.models import WebhookReceiver, WebhookReceiverGroup


class AppTest(APITestCase):
    def test_root(self):
        url = reverse("plugins-api:netbox_webhook_receiver-api:api-root")
        response = self.client.get(f"{url}?format=api", **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WebhookReceiverGroupTest(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    view_namespace = "plugins-api:netbox_webhook_receiver"
    model = WebhookReceiverGroup
    brief_fields = ["description", "display", "id", "name", "url"]
    create_data = [
        {"name": "Group 4"},
        {"name": "Group 5", "description": "Fifth group"},
        {"name": "Group 6"},
    ]
    bulk_update_data = {"description": "New description"}

    @classmethod
    def setUpTestData(cls):
        WebhookReceiverGroup.objects.bulk_create(
            [
                WebhookReceiverGroup(name="Group 1"),
                WebhookReceiverGroup(name="Group 2"),
                WebhookReceiverGroup(name="Group 3"),
            ]
        )

    def test_receivers_count(self):
        self.add_permissions("netbox_webhook_receiver.view_webhookreceivergroup")
        group = WebhookReceiverGroup.objects.get(name="Group 1")
        WebhookReceiver.objects.create(
            name="Receiver 1", receiver_group=group, token="t1"
        )
        response = self.client.get(self._get_detail_url(group), **self.header)
        self.assertEqual(response.data["receivers_count"], 1)


class WebhookReceiverTest(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    view_namespace = "plugins-api:netbox_webhook_receiver"
    model = WebhookReceiver
    brief_fields = ["description", "display", "id", "name", "url", "uuid"]
    bulk_update_data = {"description": "New description"}
    validation_excluded_fields = ["token", "secret_key"]

    @classmethod
    def setUpTestData(cls):
        group = WebhookReceiverGroup.objects.create(name="Group 1")
        WebhookReceiver.objects.bulk_create(
            [
                WebhookReceiver(name="Receiver 1", receiver_group=group, token="t1"),
                WebhookReceiver(name="Receiver 2", receiver_group=group, token="t2"),
                WebhookReceiver(name="Receiver 3", token="t3"),
            ]
        )
        cls.create_data = [
            {
                "name": "Receiver 4",
                "receiver_group": group.pk,
                "auth_method": WebhookAuthMethodChoices.TOKEN,
                "token": "t4",
            },
            {
                "name": "Receiver 5",
                "auth_method": WebhookAuthMethodChoices.SIGNATURE_VERIFICATION,
                "auth_header": "X-Hub-Signature-256",
                "secret_key": "s5",
                "hash_algorithm": HashingAlgorithmChoices.SHA_256,
            },
            {
                "name": "Receiver 6",
                "token": "t6",
                "store_payload": False,
            },
        ]

    def test_credentials_are_write_only(self):
        self.add_permissions("netbox_webhook_receiver.view_webhookreceiver")
        receiver = WebhookReceiver.objects.first()
        response = self.client.get(self._get_detail_url(receiver), **self.header)
        self.assertNotIn("token", response.data)
        self.assertNotIn("secret_key", response.data)

    def test_token_required(self):
        self.add_permissions("netbox_webhook_receiver.add_webhookreceiver")
        response = self.client.post(
            self._get_list_url(),
            {"name": "No Token", "auth_method": WebhookAuthMethodChoices.TOKEN},
            format="json",
            **self.header,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("token", response.data)

    def test_duplicate_uuid(self):
        self.add_permissions("netbox_webhook_receiver.add_webhookreceiver")
        existing = WebhookReceiver.objects.first()
        response = self.client.post(
            self._get_list_url(),
            {"name": "Duplicate", "token": "t7", "uuid": str(existing.uuid)},
            format="json",
            **self.header,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("uuid", response.data)
