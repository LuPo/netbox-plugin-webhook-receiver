from netbox.plugins import PluginMenuButton, PluginMenuItem

webhook_receiver_buttons = [
    PluginMenuButton(
        link="plugins:netbox_webhook_receiver:webhookreceiver_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
        permissions=["netbox_webhook_receiver.add_webhookreceiver"],
    )
]

webhook_receiver_group_buttons = [
    PluginMenuButton(
        link="plugins:netbox_webhook_receiver:webhookreceivergroup_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
        permissions=["netbox_webhook_receiver.add_webhookreceivergroup"],
    )
]

menu_items = (
    PluginMenuItem(
        link="plugins:netbox_webhook_receiver:webhookreceivergroup_list",
        link_text="Webhook Receiver Groups",
        permissions=["netbox_webhook_receiver.view_webhookreceivergroup"],
        buttons=webhook_receiver_group_buttons,
    ),
    PluginMenuItem(
        link="plugins:netbox_webhook_receiver:webhookreceiver_list",
        link_text="Webhook Receivers",
        permissions=["netbox_webhook_receiver.view_webhookreceiver"],
        buttons=webhook_receiver_buttons,
    ),
)
