from django.conf.urls import patterns, url
from shopify_webhook.views import WebhookView

urlpatterns = patterns('',
    url(r'webhook/', WebhookView.as_view(), name = 'webhook'),        
)
