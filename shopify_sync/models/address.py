from __future__ import unicode_literals

import shopify
from django.db import models

from .base import ShopifyResourceModel


class Address(ShopifyResourceModel):
    shopify_resource_class = shopify.resources.Address

    address1 = models.CharField(max_length = 256)
    address2 = models.CharField(max_length = 256)
    city = models.CharField(max_length = 256)
    company = models.CharField(max_length = 256, null = True)
    country = models.CharField(max_length = 256)
    country_code = models.CharField(max_length = 256)
    country_name = models.CharField(max_length = 256)
    default = models.BooleanField(default = False)
    first_name = models.CharField(max_length = 256, null = True)
    last_name = models.CharField(max_length = 256, null = True)
    phone = models.CharField(max_length = 32, null = True)
    province = models.CharField(max_length = 32, null = True)
    province_code = models.CharField(max_length = 32, null = True)
    zip = models.CharField(max_length = 16, null = True)

    class Meta:
        app_label = 'shopify_sync'
