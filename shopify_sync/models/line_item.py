from __future__ import unicode_literals

import shopify
from django.db import models
from jsonfield import JSONField

from ..encoders import ShopifyDjangoJSONEncoder, empty_list
from .base import ShopifyResourceModel


class LineItem(ShopifyResourceModel):
    shopify_resource_class = shopify.resources.LineItem
    parent_field = 'order_id'

    fulfillable_quantity = models.IntegerField()
    fulfillment_service = models.CharField(max_length = 32)
    fulfillment_status = models.CharField(max_length = 32, null = True)
    grams = models.DecimalField(max_digits = 10, decimal_places = 2)
    name = models.CharField(max_length = 256)
    order = models.ForeignKey('shopify_sync.Order', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    product_id = models.BigIntegerField(null = True)
    product_exists = models.BooleanField(default = True)
    properties = JSONField(default = empty_list, dump_kwargs = {'cls': ShopifyDjangoJSONEncoder})
    quantity = models.IntegerField()
    requires_shipping = models.BooleanField(default = True)
    sku = models.CharField(max_length = 256)
    gift_card = models.BooleanField(default = False)
    taxable = models.BooleanField(default = False)
    tax_lines = JSONField(default = empty_list, dump_kwargs = {'cls': ShopifyDjangoJSONEncoder})
    title = models.CharField(max_length = 256)
    total_discount = models.DecimalField(max_digits = 10, decimal_places = 2)
    variant_id = models.BigIntegerField(null = True)
    variant_title = models.CharField(max_length = 256, null=True)
    vendor = models.CharField(max_length=64, null=True)

    class Meta:
        app_label = 'shopify_sync'

    def fix_ids(self):
        from . import Product
        product = Product.objects.get(title=self.title)
        self.product_id = product.id

        if len(product.variants) == 1:
            self.variant_id = product.variants[0].id
        else:
            # there is more than one variant, so we look up the title
            variant = product.variant_set.get(title=self.variant_title)
            self.variant_id = variant.id
        self.save()

    def __str__(self):
        return self.name
