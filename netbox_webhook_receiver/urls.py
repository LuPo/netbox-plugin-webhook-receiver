from netbox.views.generic import ObjectChangeLogView
from django.urls import path
from . import models, views
from netbox_webhook_receiver.views import gitlab_webhook

urlpatterns = (
    # Receive Webhook Messages
    path("webhooks/gitlab/<uuid:random_path>/", gitlab_webhook),
    # Webhook Receiver
    path("receivers/", views.WebhookReceiverListView.as_view(), name="receiver_list"),
    path(
        "receivers/",
        views.WebhookReceiverListView.as_view(),
        name="webhookreceiver_list",
    ),
    path(
        "receivers/add/", views.WebhookReceiverEditView.as_view(), name="receiver_add"
    ),
    path(
        "receivers/add/",
        views.WebhookReceiverEditView.as_view(),
        name="webhookreceiver_add",
    ),
    path("receivers/<int:pk>/", views.WebhookReceiverView.as_view(), name="receiver"),
    path(
        "receivers/<int:pk>/edit/",
        views.WebhookReceiverEditView.as_view(),
        name="webhookreceiver_edit",
    ),
    path(
        "receivers/<int:pk>/delete/",
        views.WebhookReceiverDeleteView.as_view(),
        name="webhookreceiver_delete",
    ),
    path(
        "receivers/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="webhookreceiver_changelog",
        kwargs={"model": models.WebhookReceiver},
    ),
)
