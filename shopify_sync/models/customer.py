from __future__ import unicode_literals

import shopify
from django.db import models

from .address import Address
from .base import ShopifyDatedResourceModel
from .order import Order


class Customer(ShopifyDatedResourceModel):
    shopify_resource_class = shopify.resources.Customer
    related_fields = ['default_address']

    accepts_marketing = models.BooleanField(default = False)
    default_address = models.ForeignKey(Address, null = True, related_name = 'default_address')
    email = models.EmailField()
    first_name = models.CharField(max_length = 64)
    multipass_identified = models.CharField(max_length = 64, null = True)
    last_name = models.CharField(max_length = 64)
    last_order_id = models.IntegerField(null = True)
    last_order_name = models.CharField(max_length = 32, null = True)
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
        return Address.objects.filter(self.user, customer = self)

    @property
    def orders(self):
        return Order.objects.filter(self.user, customer = self)
