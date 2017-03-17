from django.conf.urls import url
from shopify_webhook.views import WebhookView

urlpatterns = (
    url(r'webhook/', WebhookView.as_view(), name='webhook'),
)
