# ruff: noqa: E501
# fmt: off
from django.urls import include, path
from utilities.urls import get_model_urls
from . import views

urlpatterns = (
    # Receive Webhook Messages
    path(
        "webhooks/<uuid:uuid>/",
        views.incoming_webhook_request,
        name="webhook",
    ),
    # Webhook Receiver
    path(
        "receivers/",
        include(get_model_urls("netbox_webhook_receiver", "webhookreceiver", detail=False)),
    ),
    path(
        "receivers/<int:pk>/",
        include(get_model_urls("netbox_webhook_receiver", "webhookreceiver")),
    ),
    # Webhook Receiver Group
    path(
        "groups/",
        include(get_model_urls("netbox_webhook_receiver", "webhookreceivergroup", detail=False)),
    ),
    path(
        "groups/<int:pk>/",
        include(get_model_urls("netbox_webhook_receiver", "webhookreceivergroup")),
    ),
)
