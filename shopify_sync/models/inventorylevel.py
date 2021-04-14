from __future__ import unicode_literals

import shopify
from django.db import models

from .base import ShopifyDatedResourceModel
from .inventoryitem import InventoryItem
from .location import Location


class InventoryLevel(ShopifyDatedResourceModel):
    # todo Inherit from ShopifyResourceModelBase instead of dated resource to avoid the ID issue
    shopify_resource_class = shopify.resources.InventoryLevel
    # parent_field = 'inventory_item_id'
    related_fields = ["location", "inventory_item"]
    r_fields = {"inventory_item_id": InventoryItem, "location_id": Location}

    inventory_item = models.ForeignKey(
        "shopify_sync.InventoryItem", on_delete=models.CASCADE
    )
    location = models.ForeignKey("shopify_sync.Location", on_delete=models.CASCADE)
    available = models.IntegerField(null=True, default=0)
    id = models.AutoField(primary_key=True)

    class Meta:
        app_label = "shopify_sync"
        unique_together = ("inventory_item", "location", "id")

    @property
    def _prefix_options(self):
        return {
            "inventory_item_id": self.inventory_item.id,
            "location_id": self.location.id,
        }

    def __str__(self):
        return "%s - %s" % (self.id, self.location_id)
