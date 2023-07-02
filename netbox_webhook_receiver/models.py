from .choices import WebhookAuthMethodChoices
from core.models import DataSource
from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
import uuid


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


class WebhookReceiverGroup(NetBoxModel):
    comments = models.TextField(blank=True)
    description = models.CharField(max_length=500, blank=True)
    name = models.CharField(
        help_text="Webhook receiver group", max_length=50, null=False
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "plugins:netbox_webhook_receiver:webhookreceivergroup", args=[self.pk]
        )


class WebhookReceiver(NetBoxModel):
    comments = models.TextField(blank=True)
    datasource = models.ForeignKey(
        to=DataSource, on_delete=models.CASCADE, blank=True, null=True
    )
    description = models.CharField(max_length=500, blank=True)
    name = models.CharField(
        help_text="Webhook receiver name", max_length=50, null=False
    )
    receiver_group = models.ForeignKey(
        to=WebhookReceiverGroup,
        on_delete=models.PROTECT,
        related_name="receivers",
        blank=True,
        null=True,
    )
    token = models.CharField(
        help_text="Token to authorize the processing", max_length=50, null=False
    )
    # Look at https://github.com/netbox-community/netbox/issues/11891
    # and https://github.com/netbox-community/netbox/pull/12675/files
    auth_header = models.CharField(  # instead of token_name
        help_text="Custom Header option token name",
        max_length=50,
        null=False,
        default="X-Gitlab-Token",
    )
    auth_method = models.CharField(  # instead of token_name
        help_text="Custom Header option token name",
        max_length=50,
        choices=WebhookAuthMethodChoices,
        default=WebhookAuthMethodChoices.SIGNATURE_VERIFICATION,
        null=False,
    )
    secret_key = models.CharField(  # instead of token_name
        help_text="Secret key for HMAC hex digest of the payload body",
        max_length=50,
        null=True,
    )
    store_payload = models.BooleanField(
        help_text="Store payload of incomming webhooks", default=True
    )
    uuid = models.UUIDField(default=uuid.uuid4)

    class Meta:
        ordering = (
            "name",
            "receiver_group",
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "plugins:netbox_webhook_receiver:webhookreceiver", args=[self.pk]
        )
