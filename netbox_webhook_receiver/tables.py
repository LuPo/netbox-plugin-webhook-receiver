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
            "description",
            "webhook_origin",
            "uuid",
            "token_name",
            "token",
        )
        default_columns = ("name", "webhook_origin", "uuid")
