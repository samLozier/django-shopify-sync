from __future__ import unicode_literals

import shopify
from django.db import models

from .base import ShopifyDatedResourceModel


class Metafield(ShopifyDatedResourceModel):
    shopify_resource_class = shopify.resources.Metafield
    parent_field = 'product_id'

    VALUE_TYPE_STRING = 'string'
    VALUE_TYPE_INTEGER = 'integer'
    VALUE_TYPE_CHOICES = (
        (VALUE_TYPE_STRING, 'String'),
        (VALUE_TYPE_INTEGER, 'Integer'),
    )

    OWNER_RESOURCE_SHOP = 'shop'
    OWNER_RESOURCE_PRODUCT = 'product'
    OWNER_RESOURCE_CHOICES = (
        (OWNER_RESOURCE_SHOP, 'Shop'),
        (OWNER_RESOURCE_PRODUCT, 'Product'),
    )

    description = models.CharField(max_length = 255, null=True)
    key = models.CharField(max_length = 30)
    namespace = models.CharField(max_length = 20)
    owner_id = models.BigIntegerField()
    owner_resource = models.CharField(max_length = 32, choices = OWNER_RESOURCE_CHOICES, default = OWNER_RESOURCE_SHOP)
    value = models.TextField()
    value_type = models.CharField(max_length = 32, choices = VALUE_TYPE_CHOICES, default = VALUE_TYPE_STRING)
    product = models.ForeignKey('shopify_sync.Product', null=True, on_delete=models.CASCADE)

    class Meta:
        app_label = 'shopify_sync'

    def __str__(self):
        return "%s=%s for %s" % (self.key, self.value, self.product,)
