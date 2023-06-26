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
            "id",
            "url",
            "display",
            "name",
            "webhook_origin",
            "token_name",
            "uuid",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
