from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField
from .models import WebhookReceiver, OriginatorChoices


class WebhookReceiverForm(NetBoxModelForm):
    # originator_type = DynamicModelChoiceField(
    #     queryset=OriginatorChoices.objects.all()
    # )
    comments = CommentField()

    class Meta:
        model = WebhookReceiver
        fields = (
            "name",
            "description",
            "originator_type",
            "uuid",
            "token_name",
            "token",
            "comments",
            "tags",
        )


class WebhookReceiverFilterForm(NetBoxModelFilterSetForm):
    model = WebhookReceiver
    # tags = TagFilterField(
    #     required=False
    # )

    originator_type = forms.MultipleChoiceField(
        choices=OriginatorChoices, required=False
    )
    uuid = forms.CharField(required=False)
