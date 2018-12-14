from __future__ import unicode_literals

import shopify
from django.db import models

from .base import ShopifyDatedResourceModel


class Variant(ShopifyDatedResourceModel):
    shopify_resource_class = shopify.resources.Variant
    parent_field = 'product_id'

    barcode = models.CharField(max_length = 255, null = True)
    compare_at_price = models.DecimalField(max_digits = 10, decimal_places = 2, null = True)
    fulfillment_service = models.CharField(max_length = 32, default = 'manual')
    grams = models.IntegerField()
    inventory_management = models.CharField(max_length = 32, null = True, default = 'blank')
    inventory_policy = models.CharField(max_length = 32, null = True, default = 'deny')
    inventory_quantity = models.IntegerField(null=True)
    option1 = models.CharField(max_length = 255, null = True)
    option2 = models.CharField(max_length = 255, null = True)
    option3 = models.CharField(max_length = 255, null = True)
    position = models.IntegerField(null = True, default = 1)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    product = models.ForeignKey('shopify_sync.Product', on_delete=models.CASCADE)
    requires_shipping = models.BooleanField(default = True)
    sku = models.CharField(max_length = 255, null = True)
    taxable = models.BooleanField(default = True)
    title = models.CharField(max_length = 255, blank=True, null=True)

    class Meta:
        app_label = 'shopify_sync'

    def __str__(self):
        return "%s - %s" % (self.product, self.title)
