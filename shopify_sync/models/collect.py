from __future__ import unicode_literals

import shopify
from django.db import models

from .base import ShopifyDatedResourceModel


class Collect(ShopifyDatedResourceModel):
    shopify_resource_class = shopify.resources.Collect

    collection_id = models.BigIntegerField()
    featured = models.BooleanField(default = False)
    position = models.IntegerField(null = True, default = 1)
    product_id = models.BigIntegerField()
    sort_value = models.CharField(max_length = 16, null = True)

    class Meta:
        app_label = 'shopify_sync'
