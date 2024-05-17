from netbox.plugins import PluginMenuButton, PluginMenuItem

webhook_receiver_buttons = [
    PluginMenuButton(
        link="plugins:netbox_webhook_receiver:webhookreceiver_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
    )
]

webhook_receiver_group_buttons = [
    PluginMenuButton(
        link="plugins:netbox_webhook_receiver:webhookreceivergroup_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
    )
]

menu_items = (
    PluginMenuItem(
        link="plugins:netbox_webhook_receiver:webhookreceivergroup_list",
        link_text="Webhook Receiver Groups",
        buttons=webhook_receiver_group_buttons,
    ),
    PluginMenuItem(
        link="plugins:netbox_webhook_receiver:webhookreceiver_list",
        link_text="Webhook Receivers",
        buttons=webhook_receiver_buttons,
    ),
)
