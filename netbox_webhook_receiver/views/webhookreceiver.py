from netbox.views import generic
from .. import filtersets, forms, models, tables


class WebhookReceiverView(generic.ObjectView):
    queryset = models.WebhookReceiver.objects.all()
    template_name = "netbox_webhook_receiver/webhookreceiver.html"


class WebhookReceiverListView(generic.ObjectListView):
    queryset = models.WebhookReceiver.objects.all()
    table = tables.WebhookReceiverTable
    filterset = filtersets.WebhookReceiverFilterSet
    filterset_form = forms.WebhookReceiverFilterForm


class WebhookReceiverEditView(generic.ObjectEditView):
    queryset = models.WebhookReceiver.objects.all()
    form = forms.WebhookReceiverForm


class WebhookReceiverDeleteView(generic.ObjectDeleteView):
    queryset = models.WebhookReceiver.objects.all()
