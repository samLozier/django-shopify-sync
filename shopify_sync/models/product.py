from __future__ import unicode_literals

import shopify
from django.db import models

from .base import ShopifyDatedResourceModel
from .collect import Collect
from .image import Image
from .option import Option
from .variant import Variant


class Product(ShopifyDatedResourceModel):
    shopify_resource_class = shopify.resources.Product
    child_fields = {
        'images': Image,
        'variants': Variant,
        'options': Option,
    }

    body_html = models.TextField()
    handle = models.CharField(max_length = 255, db_index = True)
    product_type = models.CharField(max_length = 255, db_index = True)
    published_at = models.DateTimeField(null = True)
    published_scope = models.CharField(max_length = 64, default = 'global')
    tags = models.CharField(max_length = 255, blank = True)
    template_suffix = models.CharField(max_length = 255, null = True)
    title = models.CharField(max_length = 255, db_index = True)
    vendor = models.CharField(max_length=255, db_index=True, null=True)

    class Meta:
        app_label = 'shopify_sync'

    @property
    def images(self):
        return Image.objects.filter(product_id = self.id)

    @property
    def collects(self):
        return Collect.objects.filter(product_id = self.id)

    @property
    def variants(self):
        return Variant.objects.filter(product_id = self.id)

    @property
    def options(self):
        return Option.objects.filter(product_id = self.id)

    @property
    def price(self):
        return (
            min([variant.price for variant in self.variants]),
            max([variant.price for variant in self.variants]),
        )

    @property
    def weight(self):
        return (
            min([variant.grams for variant in self.variants]),
            max([variant.grams for variant in self.variants]),
        )

    def __str__(self):
        return self.title
