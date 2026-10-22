import uuid

from django.utils import timezone
from utilities.testing import ViewTestCases, create_tags
from netbox_webhook_receiver.choices import WebhookAuthMethodChoices
from netbox_webhook_receiver.models import (
    WebhookMessage,
    WebhookReceiver,
    WebhookReceiverGroup,
)


class PluginViewTestMixin:
    def _get_base_url(self):
        return f"plugins:netbox_webhook_receiver:{self.model._meta.model_name}_{{}}"

    def test_list_has_no_dead_buttons(self):
        model_name = self.model._meta.model_name
        self.add_permissions(
            *[
                f"netbox_webhook_receiver.{action}_{model_name}"
                for action in ("view", "add", "change", "delete")
            ]
        )
        response = self.client.get(self._get_url("list"))
        self.assertHttpStatus(response, 200)
        # Actions without a registered view render as href="None"
        self.assertNotContains(response, '="None"')


class WebhookReceiverGroupTestCase(
    PluginViewTestMixin,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = WebhookReceiverGroup

    @classmethod
    def setUpTestData(cls):
        WebhookReceiverGroup.objects.bulk_create(
            [
                WebhookReceiverGroup(name="Group 1"),
                WebhookReceiverGroup(name="Group 2"),
                WebhookReceiverGroup(name="Group 3"),
            ]
        )
        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "Group X",
            "description": "A new group",
            "comments": "Some comments",
            "tags": [t.pk for t in tags],
        }


class WebhookReceiverTestCase(
    PluginViewTestMixin,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = WebhookReceiver

    @classmethod
    def setUpTestData(cls):
        group = WebhookReceiverGroup.objects.create(name="Group 1")
        WebhookReceiver.objects.bulk_create(
            [
                WebhookReceiver(name="Receiver 1", receiver_group=group, token="t1"),
                WebhookReceiver(name="Receiver 2", receiver_group=group, token="t2"),
                WebhookReceiver(name="Receiver 3", token="t3"),
            ]
        )
        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "Receiver X",
            "receiver_group": group.pk,
            "description": "A new receiver",
            "uuid": uuid.uuid4(),
            "store_payload": False,
            "auth_method": WebhookAuthMethodChoices.TOKEN,
            "auth_header": "X-Gitlab-Token",
            "token": "new-token",
            "comments": "Some comments",
            "tags": [t.pk for t in tags],
        }

    def test_group_view_lists_receivers(self):
        self.add_permissions(
            "netbox_webhook_receiver.view_webhookreceivergroup",
            "netbox_webhook_receiver.view_webhookreceiver",
        )
        group = WebhookReceiverGroup.objects.first()
        response = self.client.get(group.get_absolute_url())
        self.assertHttpStatus(response, 200)

        # The receivers table is loaded through HTMX from the filtered list view
        response = self.client.get(
            self._get_url("list"),
            {"receiver_group_id": group.pk},
            headers={"HX-Request": "true"},
        )
        self.assertHttpStatus(response, 200)
        self.assertContains(response, "Receiver 1")
        self.assertNotContains(response, "Receiver 3")

    def test_webhook_url_panel(self):
        self.add_permissions("netbox_webhook_receiver.view_webhookreceiver")
        receiver = WebhookReceiver.objects.first()
        response = self.client.get(receiver.get_absolute_url())
        self.assertHttpStatus(response, 200)
        self.assertContains(response, f"http://testserver{receiver.get_webhook_url()}")
        self.assertContains(response, 'data-clipboard-target="#webhook_url"')

    def test_payloads_tab(self):
        self.add_permissions("netbox_webhook_receiver.view_webhookreceiver")
        receiver = WebhookReceiver.objects.first()
        url = self._get_url("payloads", receiver)

        # The tab is hidden until a payload is stored
        response = self.client.get(receiver.get_absolute_url())
        self.assertNotContains(response, url)

        WebhookMessage.objects.create(
            receiver=receiver,
            received_at=timezone.now(),
            payload={"ref": "refs/heads/main"},
        )
        response = self.client.get(receiver.get_absolute_url())
        self.assertContains(response, url)

        response = self.client.get(url)
        self.assertHttpStatus(response, 200)
        self.assertContains(response, "refs/heads/main")
