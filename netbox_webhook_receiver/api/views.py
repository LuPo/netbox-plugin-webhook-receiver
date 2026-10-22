from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import WebhookReceiverSerializer, WebhookReceiverGroupSerializer


class WebhookReceiverViewSet(NetBoxModelViewSet):
    queryset = models.WebhookReceiver.objects.all()
    serializer_class = WebhookReceiverSerializer
    filterset_class = filtersets.WebhookReceiverFilterSet


class WebhookReceiverGroupViewSet(NetBoxModelViewSet):
    queryset = models.WebhookReceiverGroup.objects.all()
    serializer_class = WebhookReceiverGroupSerializer
    filterset_class = filtersets.WebhookReceiverGroupFilterSet
