from __future__ import unicode_literals

import uuid

import shopify
from django.db import models

from shopify_sync import SHOPIFY_API_PAGE_LIMIT
from .base import ShopifyResourceModelBase
from .customer import Customer


class ShopifyAddress(shopify.base.ShopifyResource):
    """
    This is here mostly to properly create related urls like /customers/1319263371346/addresses/2195309133906.json
    as Shopify doesn't let us read an address by ID without the customer prefix, and the implementation provided
    by Shopify doesn't deal with this fact
    """
    _prefix_source = "/customers/$customer_id/"
    _plural = "addresses"
    _singular = "address"

    @classmethod
    def count(cls, _options=None, **kwargs):
        return SHOPIFY_API_PAGE_LIMIT


class Address(ShopifyResourceModelBase):
    shopify_resource_class = ShopifyAddress

    related_fields = ['customer']
    r_fields = {
        'customer': Customer,
    }

    id = models.BigIntegerField(primary_key=True)  # The numbers that shopify uses are too large
    address1 = models.CharField(max_length = 256, null=True)
    address2 = models.CharField(max_length = 256, null=True)
    city = models.CharField(max_length = 256, null=True)
    company = models.CharField(max_length = 256, null = True)
    country = models.CharField(max_length = 256, null=True)
    country_code = models.CharField(max_length = 256, null=True)
    country_name = models.CharField(max_length = 256, null=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    default = models.BooleanField(default = False)
    first_name = models.CharField(max_length = 256, null = True)
    last_name = models.CharField(max_length = 256, null = True)
    phone = models.CharField(max_length = 32, null = True)
    province = models.CharField(max_length = 32, null = True)
    province_code = models.CharField(max_length = 32, null = True)
    zip = models.CharField(max_length = 32, null = True)

    def __str__(self):
        if self.customer:
            return "Address id=%s, Customer id=%s" % (self.id, self.customer_id)
        else:
            return "Address id=%s" % self.id

    @property
    def _prefix_options(self):
        return {
            'customer_id': self.customer.id
        }

    class Meta:
        app_label = 'shopify_sync'
