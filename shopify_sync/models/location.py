from __future__ import unicode_literals

import shopify
from django.db import models
from .base import ShopifyDatedResourceModel


class Location(ShopifyDatedResourceModel):
    shopify_resource_class = shopify.resources.Location

    active = models.BooleanField(null=False, default=True)
    address1 = models.CharField(max_length=500, blank=True, null=True)
    address2 = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    country_code = models.CharField(max_length=2, blank=True, null=True)
    legacy = models.BooleanField(null=False, default=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    province_code = models.CharField(max_length=2, blank=True, null=True)
    zip = models.CharField(max_length=25, blank=True, null=True)
    localized_country_name = models.CharField(max_length=100, blank=True, null=True)
    localized_province_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        app_label = "shopify_sync"

    def __str__(self):
        return "%s - %s" % (self.id, self.name)
