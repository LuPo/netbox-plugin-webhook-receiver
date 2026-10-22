from core.api.serializers import DataSourceSerializer
from netbox.api.fields import RelatedObjectCountField
from netbox.api.serializers import NetBoxModelSerializer
from ..models import WebhookReceiver, WebhookReceiverGroup


class WebhookReceiverGroupSerializer(NetBoxModelSerializer):
    receivers_count = RelatedObjectCountField("receivers")

    class Meta:
        model = WebhookReceiverGroup
        fields = (
            "id",
            "url",
            "display_url",
            "display",
            "name",
            "description",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
            "receivers_count",
        )
        brief_fields = ("id", "url", "display", "name", "description")


class WebhookReceiverSerializer(NetBoxModelSerializer):
    receiver_group = WebhookReceiverGroupSerializer(
        nested=True, required=False, allow_null=True
    )
    datasource = DataSourceSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = WebhookReceiver
        fields = (
            "id",
            "url",
            "display_url",
            "display",
            "name",
            "description",
            "receiver_group",
            "uuid",
            "store_payload",
            "auth_method",
            "auth_header",
            "token",
            "hash_algorithm",
            "secret_key",
            "datasource",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "url", "display", "name", "description", "uuid")
        extra_kwargs = {
            "token": {"write_only": True},
            "secret_key": {"write_only": True},
        }
