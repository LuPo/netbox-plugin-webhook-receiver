from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField
from .models import WebhookReceiver, WebhookReceiverGroup


class WebhookReceiverForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = WebhookReceiver
        fields = (
            "name",
            "receiver_group",
            "description",
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
