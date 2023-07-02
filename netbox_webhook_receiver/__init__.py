from extras.plugins import PluginConfig

__version__ = "0.1.2"


class NetBoxWebhookReceiverConfig(PluginConfig):
    name = "netbox_webhook_receiver"
    verbose_name = "NetBox Webhook Receiver"
    description = "Manage webhook receivers and queues related actions in NetBox"
    version = __version__
    author = "Łukasz Polański"
    author_email = "wookasz@gmail.com"
    required_settings = []
    default_settings = {}
    base_url = "webhook-receiver"


config = NetBoxWebhookReceiverConfig
