from netbox.api.viewsets import NetBoxModelViewSet

from .. import models  # , filtersets
from .serializers import WebhookReceiverSerializer


class WebhookReceiverViewSet(NetBoxModelViewSet):
    queryset = models.WebhookReceiver.objects.prefetch_related("tags")
    serializer_class = WebhookReceiverSerializer
