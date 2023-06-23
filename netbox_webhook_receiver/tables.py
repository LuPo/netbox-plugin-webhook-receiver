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
            "originator_type",
            "uuid",
            "token_name",
            "token",
        )
        default_columns = ("name", "originator_type", "uuid")
