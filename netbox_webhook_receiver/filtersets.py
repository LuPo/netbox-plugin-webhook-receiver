import django_filters
from django.db.models import Q
from core.models import DataSource
from netbox.filtersets import NetBoxModelFilterSet
from utilities.filtersets import register_filterset
from .choices import HashingAlgorithmChoices, WebhookAuthMethodChoices
from .models import WebhookReceiver, WebhookReceiverGroup


@register_filterset
class WebhookReceiverFilterSet(NetBoxModelFilterSet):
    receiver_group_id = django_filters.ModelMultipleChoiceFilter(
        queryset=WebhookReceiverGroup.objects.all(),
        label="Receiver group (ID)",
    )
    datasource_id = django_filters.ModelMultipleChoiceFilter(
        queryset=DataSource.objects.all(),
        label="Data source (ID)",
    )
    auth_method = django_filters.MultipleChoiceFilter(
        choices=WebhookAuthMethodChoices,
    )
    hash_algorithm = django_filters.MultipleChoiceFilter(
        choices=HashingAlgorithmChoices,
    )

    class Meta:
        model = WebhookReceiver
        fields = (
            "id",
            "name",
            "description",
            "uuid",
            "store_payload",
            "auth_header",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value)
        )


@register_filterset
class WebhookReceiverGroupFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = WebhookReceiverGroup
        fields = ("id", "name", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value)
        )
