from __future__ import unicode_literals

import shopify
import logging
from django.apps import apps
from django.db import models
from shopify_sync import SHOPIFY_API_PAGE_LIMIT

from .base import ShopifyDatedResourceModel

log = logging.getLogger(__name__)


class InventoryItem(ShopifyDatedResourceModel):
    shopify_resource_class = shopify.resources.InventoryItem
    child_fields = {}

    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    country_code_of_origin = models.CharField(max_length=2, null=True, blank=True)
    country_harmonized_system_codes = models.CharField(
        max_length=200, blank=True, null=True
    )
    harmonized_system_code = models.CharField(max_length=50, blank=True, null=True)
    province_code_of_origin = models.CharField(max_length=2, blank=True, null=True)
    sku = models.CharField(max_length=255, null=True)
    tracked = models.BooleanField(null=True, default=True)
    requires_shipping = models.BooleanField(null=True, default=True)
    # variant = models.OneToOneField('shopify_sync.Variant', on_delete=models.CASCADE, null=False)

    class Meta:
        app_label = "shopify_sync"

    @property
    def inventorylevels(self):
        inventorylevel = apps.get_model("shopify_sync", "InventoryLevel")
        return inventorylevel.objects.filter(inventory_item_id=self.id)

    def __str__(self):
        return "%s" % (self.sku)
