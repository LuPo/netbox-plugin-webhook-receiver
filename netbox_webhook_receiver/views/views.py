import datetime as dt
import json
import logging

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
from users.models import User

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

    # Webhook authentication
    verified = authenticate_request(request, receiver)
    if not verified:
        return HttpResponseForbidden(
            f"Incorrect {'token' if receiver.token else 'signature'} \
in {receiver.auth_header} header.",
            content_type="text/plain",
        )

    # Retain webhook payload for any future use case.
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


def authenticate_request(request, receiver) -> bool:
    """
    Auth token/signature header name is defined on individual webhook receiver.
    """
    # Custom header auth method
    if receiver.token:
        request_token = ascii(request.headers.get(receiver.auth_header, ""))
        configured_token = ascii(receiver.token)
        return compare_digest(request_token, configured_token)

    # Signature verification auth method
    elif receiver.secret_key:
        import hashlib
        import hmac

        hmac_header = request.headers.get(receiver.auth_header, "")
        hash_algorithm = receiver.hash_algorithm or "sha512"

        # Calculate hexadecimal HMAC digest
        hmac_digest = hmac.new(
            key=receiver.secret_key.encode("utf-8"),
            msg=request.body,
            digestmod=getattr(hashlib, hash_algorithm),
        ).hexdigest()

        return hmac.compare_digest(
            hmac_digest.encode("utf-8"), hmac_header.encode("utf-8")
        )

    else:
        return False


class DefaultUserRequest:
    """
    Netbox Job model requres valid user object when queueing datasource sync.
    Hardcoding default admin user
    """

    def __init__(self, userid=1):
        self.user = User.objects.get(id=userid)
