from netbox.search import SearchIndex, register_search
from .models import WebhookReceiver, WebhookReceiverGroup


@register_search
class WebhookReceiverIndex(SearchIndex):
    model = WebhookReceiver
    fields = (
        ("name", 100),
        ("description", 500),
        ("comments", 5000),
    )
    display_attrs = ("receiver_group", "auth_method", "datasource", "description")


@register_search
class WebhookReceiverGroupIndex(SearchIndex):
    model = WebhookReceiverGroup
    fields = (
        ("name", 100),
        ("description", 500),
        ("comments", 5000),
    )
    display_attrs = ("description",)
