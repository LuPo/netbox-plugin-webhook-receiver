from netbox.api.routers import NetBoxRouter
from . import views

app_name = "netbox_webhook_receiver"

router = NetBoxRouter()
router.register("receivers", views.WebhookReceiverViewSet)
router.register("groups", views.WebhookReceiverGroupViewSet)

urlpatterns = router.urls
