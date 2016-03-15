from __future__ import unicode_literals

import shopify
from django.db import models

from .base import ShopifyDatedResourceModel


class ScriptTag(ShopifyDatedResourceModel):
    shopify_resource_class = shopify.resources.ScriptTag

    event = models.CharField(max_length = 16)
    src = models.URLField()

    class Meta:
        app_label = 'shopify_sync'
