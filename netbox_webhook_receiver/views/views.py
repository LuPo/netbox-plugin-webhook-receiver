import datetime as dt
import django_rq
import json

from core.models import DataSource
from django.db.transaction import atomic, non_atomic_requests
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from netbox_webhook_receiver.models import WebhookMessage, WebhookReceiver
from secrets import compare_digest


@csrf_exempt
@require_POST
@non_atomic_requests
def gitlab_webhook(request, **kwargs):
    receiver = WebhookReceiver.objects.get(uuid=kwargs["random_path"])
    if not receiver:
        return HttpResponse(
            f"Provided path selector ({kwargs['random_path']}) is not correct"
        )

    given_token = request.headers.get(receiver.token_name, "")
    # given_token = request.headers.get("X-Gitlab-Token", "")

    if not compare_digest(given_token, receiver.token):
        return HttpResponseForbidden(
            f"Incorrect token in {receiver.token_name} header.",
            content_type="text/plain",
        )

    WebhookMessage.objects.filter(
        received_at__lte=timezone.now() - dt.timedelta(days=7)
    ).delete()
    payload = json.loads(request.body)
    WebhookMessage.objects.create(
        received_at=timezone.now(),
        payload=payload,
    )

    rq_queue = django_rq.get_queue("high", is_async=False)
    rq_queue.enqueue(process_webhook_payload_gitlab, payload)

    return HttpResponse(
        f"We have processed the synchronization request for project: {payload['project']['name']}",  # noqa: E501
        content_type="text/plain",
    )


@atomic
def process_webhook_payload_gitlab(payload):
    # TODO: It will break if you configure multiple branches and same url
    data_source = DataSource.objects.get(source_url=payload["project"]["git_http_url"])
    data_source.sync()
