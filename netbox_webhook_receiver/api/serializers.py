from rest_framework import serializers

# from ipam.api.serializers import NestedPrefixSerializer
from netbox.api.serializers import NetBoxModelSerializer  # , WritableNestedSerializer
from ..models import WebhookReceiver


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
            "store_payload",
            "tags",
            "token_name",
            "url",
            "uuid",
            "webhook_provider",
        )
