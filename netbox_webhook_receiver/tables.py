import django_tables2 as tables

from netbox.tables import NetBoxTable
from .models import WebhookReceiver, WebhookReceiverGroup


class WebhookReceiverTable(NetBoxTable):
    name = tables.Column(linkify=True)
    receiver_group = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = WebhookReceiver
        fields = (
            "pk",
            "comments",
            "name",
            "datasource",
            "description",
            "receiver_group" "store_payload",
            "auth_header",
            "auth_method",
            "secret_key",
            "token",
            "uuid",
        )
        default_columns = ("name", "receiver_group", "description", "uuid")


class WebhookReceiverGroupTable(NetBoxTable):
    name = tables.Column(linkify=True)
    receivers_count = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = WebhookReceiverGroup
        fields = (
            "pk",
            "comments",
            "name",
            "description",
            "receivers_count",
        )
        default_columns = ("name", "description", "receivers_count")
