from netbox.api.routers import NetBoxRouter
from . import views

app_name = "netbox_webhook_receiver"

router = NetBoxRouter()
router.register("receiver", views.WebhookReceiverViewSet)

urlpatterns = router.urls
