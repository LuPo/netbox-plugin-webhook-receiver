from netbox.views import generic
from .. import filtersets, forms, models, tables


class WebhookReceiverView(generic.ObjectView):
    queryset = models.WebhookReceiver.objects.all()
    template_name = "netbox_webhook_receiver/webhookreceiver.html"
    # def get_extra_context(self, request, instance):
    #     table = tables.AccessListRuleTable(instance.rules.all())
    #     table.configure(request)

    #     return {
    #         'rules_table': table,
    #     }


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


# class AccessListRuleListView(generic.ObjectListView):
#     queryset = models.AccessListRule.objects.all()
#     table = tables.AccessListRuleTable
#     filterset = filtersets.AccessListRuleFilterSet
#     filterset_form = forms.AccessListRuleFilterForm

# class AccessListRuleEditView(generic.ObjectEditView):
#     queryset = models.AccessListRule.objects.all()
#     form = forms.AccessListRuleForm

# class AccessListRuleDeleteView(generic.ObjectDeleteView):
#     queryset = models.AccessListRule.objects.all()
