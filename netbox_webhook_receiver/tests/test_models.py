from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from core.models import DataSource
from netbox_webhook_receiver.models import WebhookMessage, WebhookReceiver


class WebhookReceiverTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.datasource = DataSource.objects.create(
            name="Data Source 1", type="local", source_url="file:///tmp/"
        )
        cls.receiver = WebhookReceiver.objects.create(
            name="Receiver 1", token="t1", datasource=cls.datasource
        )

    def test_deleting_datasource_keeps_receiver(self):
        self.datasource.delete()
        self.receiver.refresh_from_db()
        self.assertIsNone(self.receiver.datasource)

    def test_deleting_receiver_deletes_payloads(self):
        WebhookMessage.objects.create(
            receiver=self.receiver, received_at=timezone.now(), payload={}
        )
        self.receiver.delete()
        self.assertFalse(WebhookMessage.objects.exists())

    def test_uuid_unique(self):
        receiver = WebhookReceiver(
            name="Receiver 2", token="t2", uuid=self.receiver.uuid
        )
        with self.assertRaises(ValidationError):
            receiver.full_clean()

    def test_long_credentials(self):
        receiver = WebhookReceiver(name="Receiver 2", token="x" * 255)
        receiver.full_clean()
