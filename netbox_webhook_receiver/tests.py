import datetime as dt
from http import HTTPStatus

from django.test import Client, override_settings, TestCase
from django.utils import timezone

from netbox_webhook_receiver.models import WebhookMessage


@override_settings(WEBHOOK_RECEIVER_TOKEN="abc123")
class AcmeWebhookTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def test_bad_method(self):
        response = self.client.get("/webhooks/gitlab/mPnBRC1qxapOAxQpWmjy4NofbgxCmXSj/")
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_missing_token(self):
        response = self.client.post(
            "/webhooks/gitlab/mPnBRC1qxapOAxQpWmjy4NofbgxCmXSj/",
        )
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert (
            response.content.decode() == "Incorrect token in Acme-Webhook-Token header."
        )

    def test_bad_token(self):
        response = self.client.post(
            "/webhooks/gitlab/mPnBRC1qxapOAxQpWmjy4NofbgxCmXSj/",
            HTTP_WEBHOOK_RECEIVER_TOKEN="def456",
        )
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert (
            response.content.decode() == "Incorrect token in Acme-Webhook-Token header."
        )

    def test_success(self):
        start = timezone.now()
        old_message = WebhookMessage.objects.create(
            received_at=start - dt.timedelta(days=100),
        )
        response = self.client.post(
            "/webhooks/gitlab/mPnBRC1qxapOAxQpWmjy4NofbgxCmXSj/",
            HTTP_WEBHOOK_RECEIVER_TOKEN="abc123",
            content_type="application/json",
            data={"this": "is a message"},
        )
        assert response.status_code == HTTPStatus.OK
        assert response.content.decode() == "Message received okay."
        assert not WebhookMessage.objects.filter(id=old_message.id).exists()
        awm = WebhookMessage.objects.get()
        assert awm.received_at >= start
        assert awm.payload == {"this": "is a message"}
