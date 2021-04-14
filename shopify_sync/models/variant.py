from __future__ import unicode_literals

import logging
import os

import shopify
from django.db import models

from .base import ShopifyDatedResourceModel
from .image import Image

log = logging.getLogger(__name__)


class Variant(ShopifyDatedResourceModel):
    shopify_resource_class = shopify.resources.Variant
    parent_field = "product_id"
    # child_fields = {'inventory_item_id': InventoryItem}
    # related_fields = [
    #     # 'image',
    #     'inventory_item_id'] # fields returned from the API?
    # r_fields = {
    #     'image_id': Image,
    #     'inventory_item_id': InventoryItem
    # }
    # child_fields = {
    #    "inventory_items": InventoryItem,
    # }

    barcode = models.CharField(max_length=255, null=True)
    compare_at_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    fulfillment_service = models.CharField(max_length=32, default="manual")
    grams = models.IntegerField()
    # inventory_item = models.OneToOneField(InventoryItem, models.SET_NULL, blank=True, null=True,)
    inventory_item_id = models.BigIntegerField(models.SET_NULL, unique=True, null=True,)
    inventory_management = models.CharField(max_length=32, null=True, default="blank")
    inventory_policy = models.CharField(max_length=32, null=True, default="deny")
    inventory_quantity = models.IntegerField(null=True)
    option1 = models.CharField(max_length=255, null=True)
    option2 = models.CharField(max_length=255, null=True)
    option3 = models.CharField(max_length=255, null=True)
    position = models.IntegerField(null=True, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey("shopify_sync.Product", on_delete=models.CASCADE)
    image = models.ForeignKey(Image, models.SET_NULL, blank=True, null=True,)
    requires_shipping = models.BooleanField(default=True)
    sku = models.CharField(max_length=255, null=True)
    taxable = models.BooleanField(default=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        app_label = "shopify_sync"

    def __str__(self):
        return "%s - %s" % (self.product, self.title)

    @property
    def _prefix_options(self) -> dict[str:int]:
        return {"product_id": self.product.id}

    def save(
        self,
        no_sale_on: bool = bool(os.environ["NO_SALE_ON"]),
        no_sale_tag: str = os.environ["NO_SALE_TAG"],
        *args,
        **kwargs
    ):
        """
        Due to breaking changes in the Shopify API >= 2020-04 it is now impossible to use compare_at_price == 0
        to filter for products that are not on sale in a smart collection. This filter is commonly used to exclude
        products that are already discounted from discount eligibility or use in sales. To re-create this functinality
        we're adding a tag (default==NonSale) to a variants product if all variants are not on sale, then using the tag in
        smart collections on shopify.

        Not on sale is defined as: compare_at_price == 0 or None or price

        :param no_sale_on : boolean, controls wheather to use this save override
        :type no_sale_on: bool
        :param no_sale_tag:
        :type no_sale_tag: str
        :param args: 
        :type args: 
        :param kwargs: 
        :type kwargs: 
        :return: 
        :rtype: 
        """

        parent_product = self.product
        if no_sale_on is True:
            super(Variant, self).save(*args, **kwargs)
            if (
                all(
                    [
                        True
                        if v.compare_at_price == 0 or v.compare_at_price == None
                        else False
                        for v in parent_product.variants
                    ]
                )
                is True
            ):
                # all variants have a "not on sale" compare_at_price
                on_sale = False
            else:
                on_sale = True

            if on_sale is False and no_sale_tag not in parent_product.tag_list:
                parent_product.add_tag(no_sale_tag)
                parent_product.save(push=True)

            if on_sale is True and no_sale_tag in parent_product.tag_list:
                parent_product.remove_tag(no_sale_tag)
                parent_product.save(push=True)
        else:
            super(Variant, self).save(*args, **kwargs)
        # log.debug("%s metafield for product %s <%s>" % (_new, self, instance))

    # @property  # wrong, needs to be a DB field
    # def inventory_items(self):
    #     return InventoryItem.objects.filter(inventory_item_id=self.id)
    #
    # @property
    # def inventory_levels(self):
    #     return InventoryLevel.objects.filter(inventory_item_id=self.inventoryitem)
    #
    # @classmethod
    # def related_models(cls):
    #     return [
    #         # apps.get_model('shopify_sync', 'Image'),
    #         apps.get_model('shopify_sync', 'InventoryItem')]
