from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
import uuid


class OriginatorChoices(ChoiceSet):
    CHOICES = [
        ("gitlab", "Gitlab", "green"),
    ]


class WebhookMessage(models.Model):
    payload = models.JSONField(default=None, null=True)
    received_at = models.DateTimeField(help_text="When we received the event.")

    class Meta:
        ordering = ["received_at"]
        indexes = [
            models.Index(fields=["received_at"]),
        ]

    def __str__(self):
        return self.received_at


class WebhookReceiver(NetBoxModel):
    comments = models.TextField(blank=True)
    description = models.CharField(max_length=500, blank=True)
    name = models.CharField(
        help_text="Webhook receiver name", max_length=50, null=False
    )
    token = models.CharField(
        help_text="Token to authorize the processing", max_length=50, null=False
    )
    token_name = models.CharField(
        help_text="Header option token name",
        max_length=50,
        null=False,
        default="X-Gitlab-Token",
    )
    webhook_origin = models.CharField(
        max_length=30,
        choices=OriginatorChoices,
        null=False,
    )
    uuid = models.UUIDField(default=uuid.uuid4)

    class Meta:
        ordering = (
            "name",
            "webhook_origin",
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "plugins:netbox_webhook_receiver:webhookreceiver", args=[self.pk]
        )
