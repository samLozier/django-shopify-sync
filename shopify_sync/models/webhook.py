from __future__ import unicode_literals

import shopify
from django.db import models
from jsonfield import JSONField

from ..encoders import ShopifyDjangoJSONEncoder
from .base import ShopifyDatedResourceModel


class Webhook(ShopifyDatedResourceModel):
    shopify_resource_class = shopify.resources.Webhook

    topic = models.CharField(max_length = 64)
    address = models.URLField()
    format = models.CharField(max_length = 4)
    fields = JSONField(null = True, dump_kwargs = {'cls': ShopifyDjangoJSONEncoder})
    metafield_namespaces = JSONField(null = True, dump_kwargs = {'cls': ShopifyDjangoJSONEncoder})

    class Meta:
        app_label = 'shopify_sync'
