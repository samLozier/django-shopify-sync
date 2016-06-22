from __future__ import unicode_literals

import shopify
from django.db import models
import uuid

from .base import ShopifyResourceModelBase, ShopifyResourceModel


class AddressBase(ShopifyResourceModelBase):
    shopify_resource_class = shopify.resources.Address

    address1 = models.CharField(max_length = 256, null=True)
    address2 = models.CharField(max_length = 256, null=True)
    city = models.CharField(max_length = 256, null=True)
    company = models.CharField(max_length = 256, null = True)
    country = models.CharField(max_length = 256, null=True)
    country_code = models.CharField(max_length = 256, null=True)
    country_name = models.CharField(max_length = 256, null=True)
    default = models.BooleanField(default = False)
    first_name = models.CharField(max_length = 256, null = True)
    last_name = models.CharField(max_length = 256, null = True)
    phone = models.CharField(max_length = 32, null = True)
    province = models.CharField(max_length = 32, null = True)
    province_code = models.CharField(max_length = 32, null = True)
    zip = models.CharField(max_length = 32, null = True)

    def __str__(self):
        return "Address id=%s" % self.id

    class Meta:
        # proxy = True
        abstract = True
        app_label = 'shopify_sync'


class Address(AddressBase):
    id = models.BigIntegerField(primary_key=True)  # The numbers that shopify uses are too large

    class Meta:
        app_label = 'shopify_sync'


class ShippingAddress(AddressBase):
    exclude_fields = ['session']
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        app_label = 'shopify_sync'
