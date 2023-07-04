from netbox.filtersets import NetBoxModelFilterSet
from .models import WebhookReceiver, WebhookReceiverGroup


class WebhookReceiverFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = WebhookReceiver
        fields = (
            "uuid",
            "store_payload",
            "receiver_group",
            "hash_algorithm",
            "auth_method",
        )

    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)


class WebhookReceiverGroupFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = WebhookReceiverGroup
        fields = ("name",)

    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)
