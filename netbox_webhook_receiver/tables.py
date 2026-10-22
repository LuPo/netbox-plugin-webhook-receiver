import django_tables2 as tables

from netbox.tables import NetBoxTable, columns
from .models import WebhookReceiver, WebhookReceiverGroup


class WebhookReceiverTable(NetBoxTable):
    name = tables.Column(linkify=True)
    receiver_group = tables.Column(linkify=True)
    datasource = tables.Column(linkify=True, verbose_name="Data source")
    store_payload = columns.BooleanColumn()
    auth_method = columns.ChoiceFieldColumn()
    hash_algorithm = columns.ChoiceFieldColumn()
    comments = columns.MarkdownColumn()
    tags = columns.TagColumn(
        url_name="plugins:netbox_webhook_receiver:webhookreceiver_list"
    )

    class Meta(NetBoxTable.Meta):
        model = WebhookReceiver
        fields = (
            "pk",
            "id",
            "name",
            "receiver_group",
            "description",
            "datasource",
            "store_payload",
            "auth_header",
            "auth_method",
            "hash_algorithm",
            "secret_key",
            "token",
            "uuid",
            "comments",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = ("name", "receiver_group", "description", "uuid")


class WebhookReceiverGroupTable(NetBoxTable):
    name = tables.Column(linkify=True)
    receivers_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_webhook_receiver:webhookreceiver_list",
        url_params={"receiver_group_id": "pk"},
        verbose_name="Receivers",
    )
    comments = columns.MarkdownColumn()
    tags = columns.TagColumn(
        url_name="plugins:netbox_webhook_receiver:webhookreceivergroup_list"
    )

    class Meta(NetBoxTable.Meta):
        model = WebhookReceiverGroup
        fields = (
            "pk",
            "id",
            "name",
            "description",
            "receivers_count",
            "comments",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = ("name", "description", "receivers_count")
