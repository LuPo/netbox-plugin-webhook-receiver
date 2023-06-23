from extras.plugins import PluginConfig

__version__ = "0.0.4"


class NetBoxWebhookReceiverConfig(PluginConfig):
    name = "netbox_webhook_receiver"
    verbose_name = "NetBox Webhook Receiver"
    description = "Manage Webhook Receiver endpoint in NetBox"
    version = __version__
    author = "Lukasz Polanski"
    author_email = "wookasz@gmail.com"
    required_settings = []
    default_settings = {}
    base_url = "webhook-receiver"


config = NetBoxWebhookReceiverConfig
