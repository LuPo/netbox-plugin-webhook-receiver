import datetime as dt
import hashlib
import hmac
import json
import logging

from django.contrib.auth import get_user_model
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotFound,
)
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from core.choices import JobStatusChoices
from core.jobs import SyncDataSourceJob
from netbox.plugins import get_plugin_config
from netbox_webhook_receiver.choices import (
    HashingAlgorithmChoices,
    WebhookAuthMethodChoices,
)
from netbox_webhook_receiver.models import WebhookMessage, WebhookReceiver

__all__ = ("incoming_webhook_request",)

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def incoming_webhook_request(request, uuid):
    """
    Validates incoming webhook path and custom header authentication.
    Calls the webhook processing function.
    """
    receiver = WebhookReceiver.objects.filter(uuid=uuid).first()
    if receiver is None:
        return HttpResponseNotFound(
            f"Provided path selector ({uuid}) is not correct",
            content_type="text/plain",
        )

    # Check if defined Authorisation header is present in the request
    if receiver.auth_header not in request.headers:
        return HttpResponseForbidden(
            f"Did not get authentication header {receiver.auth_header} in the request",
            content_type="text/plain",
        )

    # Webhook authentication
    if not authenticate_request(request, receiver):
        credential = (
            "token"
            if receiver.auth_method == WebhookAuthMethodChoices.TOKEN
            else "signature"
        )
        return HttpResponseForbidden(
            f"Incorrect {credential} in {receiver.auth_header} header.",
            content_type="text/plain",
        )

    # Retain webhook payload for any future use case.
    if receiver.store_payload:
        store_payload(request, receiver)

    result = "No action has been taken by webhook receiver"
    # So far datasource sync is the only action of the incoming webhook
    if receiver.datasource:
        result = sync_datasource(receiver.datasource)

    logger.info(result)
    return HttpResponse(
        result,
        content_type="text/plain",
    )


def store_payload(request, receiver):
    retention_days = get_plugin_config(
        "netbox_webhook_receiver", "payload_retention_days"
    )
    WebhookMessage.objects.filter(
        received_at__lte=timezone.now() - dt.timedelta(days=retention_days)
    ).delete()

    # Not every sender posts JSON (e.g. form encoded GitHub webhooks)
    try:
        payload = json.loads(request.body)
    except ValueError:
        payload = request.body.decode("utf-8", errors="replace")

    WebhookMessage.objects.create(
        receiver=receiver,
        received_at=timezone.now(),
        payload=payload,
    )


def sync_datasource(datasource):
    # A sync waiting in the queue picks up the latest changes anyway
    pending_jobs = SyncDataSourceJob.get_jobs(datasource).filter(
        status=JobStatusChoices.STATUS_PENDING
    )
    if pending_jobs.exists():
        return f"Synchronization of Data Source {datasource.name} is already queued"

    SyncDataSourceJob.enqueue(instance=datasource, user=get_job_user())

    return f"Synchronizing Data Source: {datasource.name}"


def get_job_user():
    """
    User the queued jobs are attributed to, as set by the job_user plugin setting.
    """
    username = get_plugin_config("netbox_webhook_receiver", "job_user")
    if not username:
        return None

    user = get_user_model().objects.filter(username=username, is_active=True).first()
    if user is None:
        logger.warning(f"job_user {username} does not exist or is inactive")
    return user


def authenticate_request(request, receiver) -> bool:
    """
    Auth token/signature header name is defined on individual webhook receiver.
    """
    header_value = request.headers.get(receiver.auth_header, "")

    # Custom header auth method
    if receiver.auth_method == WebhookAuthMethodChoices.TOKEN:
        if not receiver.token:
            return False
        return hmac.compare_digest(
            header_value.encode("utf-8"), receiver.token.encode("utf-8")
        )

    # Signature verification auth method
    if receiver.auth_method == WebhookAuthMethodChoices.SIGNATURE_VERIFICATION:
        if not receiver.secret_key:
            return False

        hash_algorithm = receiver.hash_algorithm or HashingAlgorithmChoices.SHA_512
        # GitHub prefixes the digest with the algorithm name, eg. 'sha256=<digest>'
        signature = header_value.removeprefix(f"{hash_algorithm}=")

        # Calculate hexadecimal HMAC digest
        hmac_digest = hmac.new(
            key=receiver.secret_key.encode("utf-8"),
            msg=request.body,
            digestmod=getattr(hashlib, hash_algorithm),
        ).hexdigest()

        return hmac.compare_digest(
            hmac_digest.encode("utf-8"), signature.encode("utf-8")
        )

    return False
