import django_tables2 as tables

from netbox.tables import NetBoxTable
from .models import WebhookReceiver


class WebhookReceiverTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = WebhookReceiver
        fields = (
            "pk",
            "comments",
            "name",
            "datasource",
            "description",
            "store_payload",
            "token_name",
            "token",
            "uuid",
            "webhook_provider",
        )
        default_columns = ("name", "webhook_provider", "uuid")
