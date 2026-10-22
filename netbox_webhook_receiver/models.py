from .choices import WebhookAuthMethodChoices, HashingAlgorithmChoices
from core.models import DataSource
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
import uuid


class WebhookMessage(models.Model):
    receiver = models.ForeignKey(
        to="WebhookReceiver",
        on_delete=models.CASCADE,
        related_name="messages",
        blank=True,
        null=True,
    )
    payload = models.JSONField(default=None, null=True)
    received_at = models.DateTimeField(help_text="When we received the event.")

    class Meta:
        ordering = ["received_at"]
        indexes = [
            models.Index(fields=["received_at"]),
        ]

    def __str__(self):
        return str(self.received_at)


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


class WebhookReceiver(NetBoxModel):
    comments = models.TextField(blank=True)
    datasource = models.ForeignKey(
        help_text="Incoming webhook triggers update of selected datasource",
        to=DataSource,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    description = models.CharField(max_length=500, blank=True)
    name = models.CharField(max_length=50, null=False)
    receiver_group = models.ForeignKey(
        to=WebhookReceiverGroup,
        on_delete=models.PROTECT,
        related_name="receivers",
        blank=True,
        null=True,
    )
    token = models.CharField(
        help_text="Authentication is mandatory. Custom field Token",
        max_length=255,
        null=True,
        blank=True,
    )

    auth_header = models.CharField(
        help_text="Custom Header option carrying authentication token",
        max_length=50,
        null=False,
        default="X-Gitlab-Token",
    )
    auth_method = models.CharField(
        help_text="Webhook authentication method",
        max_length=50,
        choices=WebhookAuthMethodChoices,
        default=WebhookAuthMethodChoices.TOKEN,
        null=False,
    )
    secret_key = models.CharField(
        help_text="Authentication is mandatory. \
            Secret key for HMAC hex digest of the payload body",
        max_length=255,
        null=True,
        blank=True,
    )
    hash_algorithm = models.CharField(
        help_text="Hashing algorithm for message authentication signature. \
            If not provided sha512 will be used",
        max_length=50,
        choices=HashingAlgorithmChoices,
        null=True,
        blank=True,
    )
    store_payload = models.BooleanField(
        help_text="Store payload of incoming webhooks", default=True
    )
    uuid = models.UUIDField(verbose_name="UUID", default=uuid.uuid4, unique=True)

    class Meta:
        ordering = (
            "name",
            "receiver_group",
        )

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        # Without a credential every incoming request would be rejected
        if self.auth_method == WebhookAuthMethodChoices.TOKEN and not self.token:
            raise ValidationError(
                {"token": "A token is required for token authentication."}
            )
        if (
            self.auth_method == WebhookAuthMethodChoices.SIGNATURE_VERIFICATION
            and not self.secret_key
        ):
            raise ValidationError(
                {"secret_key": "A secret key is required for signature verification."}
            )

    def get_webhook_url(self):
        """
        Path of the endpoint receiving webhooks for this receiver.
        """
        return reverse("plugins:netbox_webhook_receiver:webhook", args=[self.uuid])
