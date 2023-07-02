from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField
from utilities.forms.utils import get_field_value
from utilities.forms.widgets import HTMXSelect
from .choices import WebhookAuthMethodChoices
from .models import WebhookReceiver, WebhookReceiverGroup


class WebhookReceiverForm(NetBoxModelForm):
    comments = CommentField()

    fieldsets = (
        ("VLAN", ("vid", "name", "status", "role", "description", "tags")),
        ("Authentication", ("auth_method", "auth_header", "secret_key", "token")),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        auth_method = get_field_value(self, "auth_method")

        if auth_method != WebhookAuthMethodChoices.TOKEN:
            del self.fields["token"]
        if auth_method != WebhookAuthMethodChoices.SIGNATURE_VERIFICATION:
            del self.fields["secret_key"]

    class Meta:
        model = WebhookReceiver
        fields = (
            "name",
            "receiver_group",
            "description",
            "store_payload",
            "auth_method",
            "auth_header",
            "secret_key",
            "token",
            "uuid",
            "datasource",
            "tags",
            "comments",
        )
        widgets = {
            "auth_method": HTMXSelect(),
        }


class WebhookReceiverFilterForm(NetBoxModelFilterSetForm):
    model = WebhookReceiver
    # tags = TagFilterField(
    #     required=False
    # )
    uuid = forms.CharField(required=False)
    receiver_group = forms.ModelMultipleChoiceField(
        queryset=WebhookReceiverGroup.objects.all(), required=False
    )


class WebhookReceiverGroupForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = WebhookReceiverGroup
        fields = (
            "name",
            "description",
            "tags",
            "comments",
        )


class WebhookReceiverGroupFilterForm(NetBoxModelFilterSetForm):
    model = WebhookReceiverGroup
    # tags = TagFilterField(
    #     required=False
    # )
