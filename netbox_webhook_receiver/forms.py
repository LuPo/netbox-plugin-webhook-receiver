from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField
from utilities.forms.rendering import FieldSet
from utilities.forms.utils import get_field_value
from utilities.forms.widgets import HTMXSelect
from .choices import WebhookAuthMethodChoices
from .models import WebhookReceiver, WebhookReceiverGroup


class WebhookReceiverForm(NetBoxModelForm):
    comments = CommentField()

    fieldsets = (
        FieldSet(
            "name",
            "receiver_group",
            "description",
            "uuid",
            "store_payload",
            name="Webhook definition",
        ),
        FieldSet(
            "auth_method",
            "auth_header",
            "secret_key",
            "token",
            "hash_algorithm",
            name="Authentication",
        ),
        FieldSet("datasource", name="Trigger action"),
        FieldSet("tags", name="Extra"),
    )

    # Thanks to Dillon Henschen for his netbox pull #12675
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        auth_method = get_field_value(self, "auth_method")

        if auth_method != WebhookAuthMethodChoices.TOKEN:
            del self.fields["token"]
            self.fields[
                "auth_header"
            ].help_text = "Custom Header option carying \
                payload signature (eg. 'X-Hub-Signature')."
        if auth_method != WebhookAuthMethodChoices.SIGNATURE_VERIFICATION:
            del self.fields["hash_algorithm"]
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
            "hash_algorithm",
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

    def clean(self):
        super().clean()

        auth_method = self.cleaned_data.get("auth_method")

        if auth_method != WebhookAuthMethodChoices.TOKEN:
            self.cleaned_data["token"] = None

        if auth_method != WebhookAuthMethodChoices.SIGNATURE_VERIFICATION:
            self.cleaned_data["secret_key"] = None


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
