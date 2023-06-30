import datetime as dt
import json
import logging

from django.contrib.auth.models import User
from django.db.transaction import atomic, non_atomic_requests
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotFound,
)
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from netbox_webhook_receiver.models import WebhookMessage, WebhookReceiver
from secrets import compare_digest

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
@non_atomic_requests
def incomming_webhook_request(request, **kwargs):
    """
    Validates incomming webhook path and custom header authentication.
    Calls the webhook processing function.
    """
    try:
        receiver = WebhookReceiver.objects.get(uuid=kwargs["random_path"])
    except WebhookReceiver.DoesNotExist:
        return HttpResponseNotFound(
            f"Provided path selector ({kwargs['random_path']}) is not correct"
        )

    # Auth token name is defined on individual webhook receiver. "X-Gitlab-Token"
    given_token = request.headers.get(receiver.token_name, "")
    if not compare_digest(given_token, receiver.token):
        return HttpResponseForbidden(
            f"Incorrect token in {receiver.token_name} header.",
            content_type="text/plain",
        )

    # Decide to store webhook payload for any reason in the future.
    if receiver.store_payload:
        WebhookMessage.objects.filter(
            received_at__lte=timezone.now() - dt.timedelta(days=2)
        ).delete()
        payload = json.loads(request.body)
        WebhookMessage.objects.create(
            received_at=timezone.now(),
            payload=payload,
        )

    result = "No action has been taken by webhook receiver"
    # So far datasource sync is the only action of the incomming webhook
    if receiver.datasource:
        # Prevent queuing multiple syncronizzation requestes
        if job := receiver.datasource.jobs.first():
            if job.status == "pending":
                return HttpResponseForbidden(
                    "There are already pending jobs in the queue",
                    content_type="text/plain",
                )

        result = process_webhook_sync_datasource(receiver)

    logger.info(result)
    return HttpResponse(
        result,
        content_type="text/plain",
    )


@atomic
def process_webhook_sync_datasource(receiver):
    receiver.datasource.enqueue_sync_job(request=DefaultUserRequest())

    return f"Synchronizing Data Source: {receiver.datasource.name}"


class DefaultUserRequest:
    """
    Netbox Job model requres valid user object when queueing datasource sync.
    Hardcoding default admin user
    """

    def __init__(self, userid=1):
        self.user = User.objects.get(id=userid)
