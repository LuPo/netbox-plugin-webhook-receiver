from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField
from .models import WebhookReceiver, OriginatorChoices


class WebhookReceiverForm(NetBoxModelForm):
    # webhook_provider = DynamicModelChoiceField(
    #     queryset=OriginatorChoices.objects.all()
    # )
    comments = CommentField()

    class Meta:
        model = WebhookReceiver
        fields = (
            "name",
            "description",
            "webhook_provider",
            "store_payload",
            "token_name",
            "token",
            "uuid",
            "datasource",
            "tags",
            "comments",
        )


class WebhookReceiverFilterForm(NetBoxModelFilterSetForm):
    model = WebhookReceiver
    # tags = TagFilterField(
    #     required=False
    # )

    webhook_provider = forms.MultipleChoiceField(
        choices=OriginatorChoices, required=False
    )
    uuid = forms.CharField(required=False)
