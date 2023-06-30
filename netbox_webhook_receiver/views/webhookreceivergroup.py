from django.db.models import Count
from netbox.views import generic
from .. import filtersets, forms, models, tables


class WebhookReceiverGroupView(generic.ObjectView):
    queryset = models.WebhookReceiverGroup.objects.all()

    def get_extra_context(self, request, instance):
        table = tables.WebhookReceiverTable(instance.receivers.all())
        table.configure(request)
        return {
            "receivers_table": table,
        }


class WebhookReceiverGroupListView(generic.ObjectListView):
    queryset = models.WebhookReceiverGroup.objects.all()
    table = tables.WebhookReceiverGroupTable
    filterset = filtersets.WebhookReceiverGroupFilterSet
    filterset_form = forms.WebhookReceiverGroupFilterForm
    queryset = models.WebhookReceiverGroup.objects.annotate(
        receivers_count=Count("receivers")
    )


class WebhookReceiverGroupEditView(generic.ObjectEditView):
    queryset = models.WebhookReceiverGroup.objects.all()
    form = forms.WebhookReceiverGroupForm


class WebhookReceiverGroupDeleteView(generic.ObjectDeleteView):
    queryset = models.WebhookReceiverGroup.objects.all()
