from netbox.filtersets import NetBoxModelFilterSet
from .models import WebhookReceiver


class WebhookReceiverFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = WebhookReceiver
        fields = ("originator_type", "uuid")

    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)
