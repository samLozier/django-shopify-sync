from __future__ import unicode_literals

import shopify
import logging
from django.db import models

from .base import ShopifyDatedResourceModel
from .collect import Collect
from .image import Image
from .option import Option
from .variant import Variant
from .metafield import Metafield
from .session import activate_session

log = logging.getLogger(__name__)


class Product(ShopifyDatedResourceModel):
    shopify_resource_class = shopify.resources.Product
    child_fields = {
        'images': Image,
        'variants': Variant,
        'options': Option,
        'metafields': Metafield,
    }

    body_html = models.TextField(default='', null=True)
    handle = models.CharField(max_length=255, db_index=True)
    product_type = models.CharField(max_length=255, db_index=True)
    published_at = models.DateTimeField(null=True)
    published_scope = models.CharField(max_length=64, default='global')
    tags = models.CharField(max_length=255, blank=True)
    template_suffix = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, db_index=True)
    vendor = models.CharField(max_length=255, db_index=True, null=True)

    class Meta:
        app_label = 'shopify_sync'

    @property
    def images(self):
        return Image.objects.filter(product_id=self.id)

    @property
    def collects(self):
        return Collect.objects.filter(product_id=self.id)

    @property
    def variants(self):
        return Variant.objects.filter(product_id=self.id)

    @property
    def options(self):
        return Option.objects.filter(product_id=self.id)

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

    def _get_tag_list(self):
        # Tags are comma-space delimited.
        # https://help.shopify.com/api/reference/product#tags-property
        return self.tags.split(', ') if self.tags else []

    def _set_tag_list(self, tag_list):
        # we need to make sure tag_list is a list, if it is not we will make it
        # one and we will use join to save to tags. The idea is that tag_list
        # will match self.tags at all time. DOESN'T AUTO SAVE
        self.tags = ', '.join(tag_list if isinstance(tag_list, list) else [tag_list])
        return self.tags
    tag_list = property(_get_tag_list, _set_tag_list)

    def add_tag(self, tag):
        # Add a tag or a list of tags
        if tag:
            self.tag_list += tag if isinstance(tag, list) else [tag]

    def remove_tag(self, tag):
        # remove all instances of a tag or list of tags
        if tag:
            rm_list = tag if isinstance(tag, list) else [tag]
            self.tag_list = [tag_ for tag_ in self.tag_list if tag_ not in rm_list]

    def save(self, sync_meta=False, *args, **kwargs):
        with activate_session(self) as shopify_resource:
            # only want to sync the metafields if we have it set to true
            metafields = shopify_resource.metafields() if sync_meta else []
            for metafield in metafields:
                defaults = metafield.attributes
                defaults.update({'product': self, 'session': self.session})
                instance, created = Metafield.objects.update_or_create(id=defaults['id'],
                                                                       defaults=defaults)
                _new = "Created" if created else "Updated"
                log.debug("%s metafield for product %s <%s>" % (_new, self, instance))
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
