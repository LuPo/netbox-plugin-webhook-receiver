from netbox.plugins import PluginConfig

__version__ = "0.6.0"


class NetBoxWebhookReceiverConfig(PluginConfig):
    name = "netbox_webhook_receiver"
    verbose_name = "NetBox Webhook Receiver"
    description = "Manage webhook receivers and queues related actions in NetBox"
    version = __version__
    author = "Łukasz Polański"
    author_email = "wookasz@gmail.com"
    base_url = "webhook-receiver"
    min_version = "4.7.0"
    required_settings = []
    default_settings = {
        # Username the queued jobs are attributed to. Jobs have no user when unset.
        "job_user": None,
        # Number of days to keep stored webhook payloads
        "payload_retention_days": 2,
    }


config = NetBoxWebhookReceiverConfig
