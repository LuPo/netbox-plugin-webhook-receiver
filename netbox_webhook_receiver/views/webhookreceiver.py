from extras.ui.panels import CustomFieldsPanel, TagsPanel
from netbox.object_actions import AddObject, BulkDelete, BulkExport
from netbox.ui import layout
from netbox.ui.breadcrumbs import Breadcrumb
from netbox.ui.panels import CommentsPanel
from netbox.views import generic
from utilities.views import ViewTab, register_model_view
from .. import filtersets, forms, models, tables
from ..ui import panels

__all__ = (
    "WebhookReceiverBulkDeleteView",
    "WebhookReceiverDeleteView",
    "WebhookReceiverEditView",
    "WebhookReceiverListView",
    "WebhookReceiverPayloadsView",
    "WebhookReceiverView",
)


@register_model_view(models.WebhookReceiver)
class WebhookReceiverView(generic.ObjectView):
    queryset = models.WebhookReceiver.objects.all()
    template_name = "generic/object.html"
    layout = layout.SimpleLayout(
        breadcrumbs=[Breadcrumb("receiver_group")],
        left_panels=[
            panels.WebhookReceiverPanel(),
            panels.WebhookAuthenticationPanel(),
            CustomFieldsPanel(),
        ],
        right_panels=[
            panels.WebhookActionsPanel(),
            TagsPanel(),
            CommentsPanel(),
        ],
        bottom_panels=[
            panels.WebhookURLPanel(),
        ],
    )


@register_model_view(models.WebhookReceiver, "payloads")
class WebhookReceiverPayloadsView(generic.ObjectView):
    queryset = models.WebhookReceiver.objects.all()
    template_name = "generic/object.html"
    tab = ViewTab(
        label="Payloads",
        badge=lambda obj: obj.messages.count(),
        weight=500,
        hide_if_empty=True,
    )
    layout = layout.Layout(
        layout.Row(
            layout.Column(
                panels.WebhookPayloadsPanel(),
            ),
        ),
    )


@register_model_view(models.WebhookReceiver, "list", path="", detail=False)
class WebhookReceiverListView(generic.ObjectListView):
    queryset = models.WebhookReceiver.objects.all()
    table = tables.WebhookReceiverTable
    filterset = filtersets.WebhookReceiverFilterSet
    filterset_form = forms.WebhookReceiverFilterForm
    # Bulk import and edit views aren't provided
    actions = (AddObject, BulkExport, BulkDelete)


@register_model_view(models.WebhookReceiver, "add", detail=False)
@register_model_view(models.WebhookReceiver, "edit")
class WebhookReceiverEditView(generic.ObjectEditView):
    queryset = models.WebhookReceiver.objects.all()
    form = forms.WebhookReceiverForm


@register_model_view(models.WebhookReceiver, "delete")
class WebhookReceiverDeleteView(generic.ObjectDeleteView):
    queryset = models.WebhookReceiver.objects.all()


@register_model_view(models.WebhookReceiver, "bulk_delete", path="delete", detail=False)
class WebhookReceiverBulkDeleteView(generic.BulkDeleteView):
    queryset = models.WebhookReceiver.objects.all()
    filterset = filtersets.WebhookReceiverFilterSet
    table = tables.WebhookReceiverTable
