from netbox.api.viewsets import NetBoxModelViewSet
from django.db.models import Count

from .. import models  # , filtersets
from .serializers import WebhookReceiverSerializer, WebhookReceiverGroupSerializer


class WebhookReceiverViewSet(NetBoxModelViewSet):
    queryset = models.WebhookReceiver.objects.prefetch_related("tags")
    serializer_class = WebhookReceiverSerializer


class WebhookReceiverGroupViewSet(NetBoxModelViewSet):
    queryset = models.WebhookReceiverGroup.objects.prefetch_related("tags").annotate(
        rule_count=Count("receivers")
    )
    serializer_class = WebhookReceiverGroupSerializer
