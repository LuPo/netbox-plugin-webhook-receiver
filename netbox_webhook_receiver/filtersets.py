from netbox.filtersets import NetBoxModelFilterSet
from .models import WebhookReceiver


class WebhookReceiverFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = WebhookReceiver
        fields = ("webhook_provider", "uuid", "store_payload")

    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)
