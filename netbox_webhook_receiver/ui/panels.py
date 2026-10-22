from netbox.ui import actions, attrs, panels

__all__ = (
    "WebhookActionsPanel",
    "WebhookAuthenticationPanel",
    "WebhookPayloadsPanel",
    "WebhookReceiverPanel",
    "WebhookURLPanel",
)


class WebhookReceiverPanel(panels.ObjectAttributesPanel):
    title = "Webhook Receiver"

    name = attrs.TextAttr("name")
    description = attrs.TextAttr("description")
    receiver_group = attrs.RelatedObjectAttr("receiver_group", linkify=True)
    uuid = attrs.TextAttr("uuid", label="UUID", style="font-monospace")


class WebhookAuthenticationPanel(panels.ObjectAttributesPanel):
    title = "Authentication"

    auth_method = attrs.ChoiceAttr("auth_method", label="Method")
    auth_header = attrs.TextAttr("auth_header", label="Header", style="font-monospace")
    token = attrs.TextAttr("token", style="font-monospace")
    hash_algorithm = attrs.ChoiceAttr("hash_algorithm", label="Hash algorithm")
    secret_key = attrs.TextAttr(
        "secret_key", label="Secret key", style="font-monospace"
    )


class WebhookActionsPanel(panels.ObjectAttributesPanel):
    title = "Webhook actions"

    store_payload = attrs.BooleanAttr("store_payload")
    datasource = attrs.RelatedObjectAttr(
        "datasource", linkify=True, label="Synchronize data source"
    )


class WebhookURLPanel(panels.ObjectPanel):
    """
    Absolute URL to configure as the webhook target on the sending side.
    """

    template_name = "netbox_webhook_receiver/panels/webhook_url.html"
    title = "Webhook Receiver URL"
    actions = [actions.CopyContent("webhook_url")]

    def get_context(self, context):
        ctx = super().get_context(context)
        return {
            **ctx,
            "webhook_url": ctx["request"].build_absolute_uri(
                ctx["object"].get_webhook_url()
            ),
        }


class WebhookPayloadsPanel(panels.ObjectPanel):
    """
    Most recent payloads stored for the receiver.
    """

    template_name = "netbox_webhook_receiver/panels/payloads.html"
    title = "Stored payloads"
    max_payloads = 20

    def get_context(self, context):
        ctx = super().get_context(context)
        messages = ctx["object"].messages.order_by("-received_at")
        return {
            **ctx,
            "payloads": list(messages[: self.max_payloads]),
            "total": messages.count(),
        }
