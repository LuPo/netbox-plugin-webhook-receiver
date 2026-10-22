from django import forms
from core.models import DataSource
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES
from utilities.forms.fields import (
    CommentField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
)
from utilities.forms.rendering import FieldSet
from utilities.forms.utils import get_field_value
from utilities.forms.widgets import HTMXSelect
from .choices import HashingAlgorithmChoices, WebhookAuthMethodChoices
from .models import WebhookReceiver, WebhookReceiverGroup


class WebhookReceiverForm(NetBoxModelForm):
    receiver_group = DynamicModelChoiceField(
        queryset=WebhookReceiverGroup.objects.all(),
        required=False,
    )
    datasource = DynamicModelChoiceField(
        queryset=DataSource.objects.all(),
        required=False,
        label="Data source",
        help_text="Incoming webhook triggers synchronization of this data source",
    )
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
            self.fields["auth_header"].help_text = "Custom Header option carrying \
                payload signature (eg. 'X-Hub-Signature-256')."
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
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet("receiver_group_id", "uuid", "store_payload", name="Attributes"),
        FieldSet("auth_method", "auth_header", "hash_algorithm", name="Authentication"),
        FieldSet("datasource_id", name="Trigger action"),
    )
    receiver_group_id = DynamicModelMultipleChoiceField(
        queryset=WebhookReceiverGroup.objects.all(),
        required=False,
        label="Receiver group",
    )
    uuid = forms.UUIDField(required=False, label="UUID")
    store_payload = forms.NullBooleanField(
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    auth_method = forms.MultipleChoiceField(
        choices=WebhookAuthMethodChoices,
        required=False,
    )
    auth_header = forms.CharField(required=False)
    hash_algorithm = forms.MultipleChoiceField(
        choices=HashingAlgorithmChoices,
        required=False,
    )
    datasource_id = DynamicModelMultipleChoiceField(
        queryset=DataSource.objects.all(),
        required=False,
        label="Data source",
    )
    tag = TagFilterField(model)


class WebhookReceiverGroupForm(NetBoxModelForm):
    comments = CommentField()

    fieldsets = (FieldSet("name", "description", "tags"),)

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
    fieldsets = (FieldSet("q", "filter_id", "tag"),)
    tag = TagFilterField(model)
