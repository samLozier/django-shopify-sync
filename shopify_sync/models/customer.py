from __future__ import unicode_literals

import shopify
from django.apps import apps
from django.db import models

from .base import ShopifyDatedResourceModel


class Customer(ShopifyDatedResourceModel):
    shopify_resource_class = shopify.resources.Customer

    accepts_marketing = models.BooleanField(default = False)
    email = models.EmailField(null=True)
    first_name = models.CharField(max_length=128, null=True)
    multipass_identified = models.CharField(max_length=128, null = True)
    last_name = models.CharField(max_length=128, null=True)
    last_order_id = models.BigIntegerField(null = True)
    last_order_name = models.CharField(max_length=128, null = True)
    note = models.TextField(null = True)
    orders_count = models.IntegerField()
    state = models.CharField(max_length = 32)
    tags = models.TextField()
    total_spent = models.DecimalField(max_digits = 10, decimal_places = 2)
    verified_email = models.BooleanField(default = False)

    class Meta:
        app_label = 'shopify_sync'

    @property
    def addresses(self):
        address = apps.get_model('shopify_sync', 'Address')
        return address.objects.filter(customer=self)

    @property
    def default_address(self):
        address = apps.get_model('shopify_sync', 'Address')
        try:
            return address.objects.get(customer=self, default=True)
        except address.DoesNotExist:
            return None

    @classmethod
    def related_models(cls):
        return [apps.get_model('shopify_sync', 'Address')]

    @property
    def orders(self):
        from .order import Order
        return Order.objects.filter(customer=self)

    def __str__(self):
        return "%s %s" % (self.first_name or "", self.last_name or "",)
