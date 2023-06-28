# ruff: noqa: E501
# fmt: off
from netbox.views.generic import ObjectChangeLogView
from django.urls import path
from . import models, views
from netbox_webhook_receiver.views import incomming_webhook_request

urlpatterns = (
    # Receive Webhook Messages
    path("webhooks/<uuid:random_path>/", incomming_webhook_request),
    # Webhook Receiver
    path("receivers/", views.WebhookReceiverListView.as_view(), name="webhookreceiver_list",),
    path("receivers/add/", views.WebhookReceiverEditView.as_view(), name="webhookreceiver_add",),
    path("receivers/<int:pk>/", views.WebhookReceiverView.as_view(), name="webhookreceiver",),
    path("receivers/<int:pk>/edit/", views.WebhookReceiverEditView.as_view(), name="webhookreceiver_edit",),
    path("receivers/<int:pk>/delete/", views.WebhookReceiverDeleteView.as_view(), name="webhookreceiver_delete",),
    path("receivers/<int:pk>/changelog/", ObjectChangeLogView.as_view(),
        name="webhookreceiver_changelog",
        kwargs={"model": models.WebhookReceiver},
    ),
)
