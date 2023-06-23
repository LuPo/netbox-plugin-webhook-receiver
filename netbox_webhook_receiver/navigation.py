from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

webhook_receiver_buttons = [
    PluginMenuButton(
        link="plugins:netbox_webhook_receiver:receiver_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
        color=ButtonColorChoices.GREEN,
    )
]

menu_items = (
    PluginMenuItem(
        link="plugins:netbox_webhook_receiver:receiver_list",
        link_text="Webhook Receiver",
        buttons=webhook_receiver_buttons,
    ),
)
