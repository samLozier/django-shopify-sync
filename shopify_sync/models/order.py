from __future__ import unicode_literals

import shopify
from django.db import models
from jsonfield import JSONField

from ..encoders import ShopifyDjangoJSONEncoder, empty_list
from .base import ShopifyDatedResourceModel
from .line_item import LineItem


class Order(ShopifyDatedResourceModel):
    shopify_resource_class = shopify.resources.Order
    related_fields = ['customer']
    child_fields = {
        'line_items': LineItem,
    }

    billing_address = JSONField(dump_kwargs = {'cls': ShopifyDjangoJSONEncoder})
    browser_ip = models.GenericIPAddressField(null = True)
    buyer_accepts_marketing = models.BooleanField(default = False)
    cancel_reason = models.CharField(max_length = 32, null = True)
    cancelled_at = models.DateTimeField(null = True)
    cart_token = models.CharField(max_length = 32, null = True)
    client_details = JSONField(dump_kwargs = {'cls': ShopifyDjangoJSONEncoder})
    closed_at = models.DateTimeField(null = True)
    currency = models.CharField(max_length = 3)
    customer = models.ForeignKey('shopify_sync.Customer', null=True)
    discount_codes = JSONField(default = empty_list, dump_kwargs = {'cls': ShopifyDjangoJSONEncoder})
    email = models.EmailField()
    financial_status = models.CharField(max_length = 32)
    fulfillment_status = models.CharField(max_length = 32, null = True)
    tags = models.TextField()
    landing_site = models.URLField(max_length=2048, null=True)
    name = models.CharField(max_length = 32)
    note = models.TextField(null = True)
    note_attributes = JSONField(dump_kwargs = {'cls': ShopifyDjangoJSONEncoder})
    number = models.IntegerField()
    order_number = models.BigIntegerField()
    processed_at = models.DateTimeField()
    processing_method = models.CharField(max_length = 32)
    referring_site = models.URLField(max_length = 2048, null = True)
    shipping_address = JSONField(null = True, dump_kwargs = {'cls': ShopifyDjangoJSONEncoder})
    shipping_lines = JSONField(default = empty_list, dump_kwargs = {'cls': ShopifyDjangoJSONEncoder})
    source_name = models.CharField(max_length = 32)
    tax_lines = JSONField(default = empty_list, dump_kwargs = {'cls': ShopifyDjangoJSONEncoder})
    taxes_included = models.BooleanField(default = True)
    token = models.CharField(max_length = 32)
    total_discounts = models.DecimalField(max_digits = 10, decimal_places = 2)
    total_line_items_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    total_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    total_tax = models.DecimalField(max_digits = 10, decimal_places = 2)
    total_weight = models.DecimalField(max_digits = 10, decimal_places = 2)

    class Meta:
        app_label = 'shopify_sync'

    @property
    def fulfillments(self):
        return []

    @property
    def line_items(self):
        return LineItem.objects.filter(self.user, order = self)

    @property
    def refund(self):
        return []

    def __str__(self):
        return self.name
