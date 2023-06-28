import datetime as dt
import json
import logging

from django.contrib.auth.models import User

# from rq.timeouts import JobTimeoutException
# from core.models import DataSource
from django.db.transaction import atomic, non_atomic_requests
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from netbox_webhook_receiver.models import WebhookMessage, WebhookReceiver
from secrets import compare_digest

logger = logging.getLogger(__name__)


class UserRequest:
    """
    Netbox Job model requres valid user object when queueing datasource sync.
    Hardcoding default user
    """

    def __init__(self, userid=1):
        self.user = User.objects.get(id=userid)


@csrf_exempt
@require_POST
@non_atomic_requests
def incomming_webhook_request(request, **kwargs):
    receiver = WebhookReceiver.objects.get(uuid=kwargs["random_path"])
    result = "No action has been taken by webhook receiver"
    if not receiver:
        return HttpResponse(
            f"Provided path selector ({kwargs['random_path']}) is not correct"
        )

    # Auth token name is defined on individual webhook receiver. "X-Gitlab-Token"
    given_token = request.headers.get(receiver.token_name, "")
    if not compare_digest(given_token, receiver.token):
        return HttpResponseForbidden(
            f"Incorrect token in {receiver.token_name} header.",
            content_type="text/plain",
        )

    if receiver.store_payload:
        WebhookMessage.objects.filter(
            received_at__lte=timezone.now() - dt.timedelta(days=2)
        ).delete()
        payload = json.loads(request.body)
        WebhookMessage.objects.create(
            received_at=timezone.now(),
            payload=payload,
        )

    if receiver.datasource:
        # Prevent queuing multiple syncronizzation requestes
        if receiver.datasource.jobs.first().status == "pending":
            return HttpResponse(
                "There are already pending jobs in the queue",
                content_type="text/plain",
            )

        result = process_webhook(receiver)

    logger.info(result)
    return HttpResponse(
        result,
        content_type="text/plain",
    )


@atomic
def process_webhook(receiver):
    dummy_request = UserRequest()
    receiver.datasource.enqueue_sync_job(request=dummy_request)
    # DataSource.objects.filter(pk=receiver.datasource.pk).update(status="failed")

    return f"Synchronizing Data Source: {receiver.datasource.name}"
