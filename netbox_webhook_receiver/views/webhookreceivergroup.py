from extras.ui.panels import CustomFieldsPanel, TagsPanel
from netbox.object_actions import AddObject, BulkDelete, BulkExport
from netbox.ui import actions, layout
from netbox.ui.panels import (
    CommentsPanel,
    ObjectsTablePanel,
    OrganizationalObjectPanel,
)
from netbox.views import generic
from utilities.query import count_related
from utilities.views import register_model_view
from .. import filtersets, forms, models, tables

__all__ = (
    "WebhookReceiverGroupBulkDeleteView",
    "WebhookReceiverGroupDeleteView",
    "WebhookReceiverGroupEditView",
    "WebhookReceiverGroupListView",
    "WebhookReceiverGroupView",
)


@register_model_view(models.WebhookReceiverGroup)
class WebhookReceiverGroupView(generic.ObjectView):
    queryset = models.WebhookReceiverGroup.objects.all()
    template_name = "generic/object.html"
    layout = layout.SimpleLayout(
        left_panels=[
            OrganizationalObjectPanel(),
            TagsPanel(),
        ],
        right_panels=[
            CustomFieldsPanel(),
            CommentsPanel(),
        ],
        bottom_panels=[
            ObjectsTablePanel(
                "netbox_webhook_receiver.webhookreceiver",
                filters={"receiver_group_id": lambda ctx: ctx["object"].pk},
                exclude_columns=["receiver_group"],
                actions=[
                    actions.AddObject(
                        "netbox_webhook_receiver.webhookreceiver",
                        url_params={"receiver_group": lambda ctx: ctx["object"].pk},
                        label="Add Webhook Receiver",
                    ),
                ],
            ),
        ],
    )


@register_model_view(models.WebhookReceiverGroup, "list", path="", detail=False)
class WebhookReceiverGroupListView(generic.ObjectListView):
    queryset = models.WebhookReceiverGroup.objects.annotate(
        receivers_count=count_related(models.WebhookReceiver, "receiver_group")
    )
    table = tables.WebhookReceiverGroupTable
    filterset = filtersets.WebhookReceiverGroupFilterSet
    filterset_form = forms.WebhookReceiverGroupFilterForm
    # Bulk import and edit views aren't provided
    actions = (AddObject, BulkExport, BulkDelete)


@register_model_view(models.WebhookReceiverGroup, "add", detail=False)
@register_model_view(models.WebhookReceiverGroup, "edit")
class WebhookReceiverGroupEditView(generic.ObjectEditView):
    queryset = models.WebhookReceiverGroup.objects.all()
    form = forms.WebhookReceiverGroupForm


@register_model_view(models.WebhookReceiverGroup, "delete")
class WebhookReceiverGroupDeleteView(generic.ObjectDeleteView):
    queryset = models.WebhookReceiverGroup.objects.all()


@register_model_view(
    models.WebhookReceiverGroup, "bulk_delete", path="delete", detail=False
)
class WebhookReceiverGroupBulkDeleteView(generic.BulkDeleteView):
    queryset = models.WebhookReceiverGroup.objects.annotate(
        receivers_count=count_related(models.WebhookReceiver, "receiver_group")
    )
    filterset = filtersets.WebhookReceiverGroupFilterSet
    table = tables.WebhookReceiverGroupTable
