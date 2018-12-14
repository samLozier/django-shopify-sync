from __future__ import unicode_literals

import shopify
from django.db import models

from .base import ShopifyResourceModel


class Option(ShopifyResourceModel):
    shopify_resource_class = shopify.resources.Option
    parent_field = 'product_id'

    name = models.CharField(max_length = 255)
    position = models.IntegerField(null = True, default = 1)
    product = models.ForeignKey('shopify_sync.Product', on_delete=models.CASCADE)

    class Meta:
        app_label = 'shopify_sync'
