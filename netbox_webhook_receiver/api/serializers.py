from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from ..models import WebhookReceiver, WebhookReceiverGroup


class WebhookReceiverSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_webhook_receiver-api:webhookreceiver-detail"
    )

    class Meta:
        model = WebhookReceiver
        fields = (
            "custom_fields",
            "created",
            "datasource",
            "last_updated",
            "id",
            "display",
            "name",
            "receiver_group",
            "store_payload",
            "tags",
            "auth_header",
            "auth_method",
            "hash_algorithm",
            "url",
            "uuid",
        )


class WebhookReceiverGroupSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_webhook_receiver-api:webhookreceivergroup-detail"
    )
    receivers_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = WebhookReceiverGroup
        fields = (
            "created",
            "last_updated",
            "id",
            "display",
            "name",
            "tags",
            "description",
            "receivers_count",
            "url",
        )
