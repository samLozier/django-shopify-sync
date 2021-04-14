from __future__ import unicode_literals

import shopify
from django.db import models
from django_hint import QueryType
from jsonfield import JSONField

from .base import ShopifyResourceModel
from .collect import Collect
from ..encoders import ShopifyDjangoJSONEncoder


class CustomCollection(ShopifyResourceModel):
    shopify_resource_class = shopify.resources.CustomCollection

    body_html = models.TextField(null=True)
    handle = models.CharField(max_length=255)
    image = JSONField(null=True, dump_kwargs={"cls": ShopifyDjangoJSONEncoder})
    published = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True)
    published_scope = models.CharField(max_length=16, default="global")
    sort_order = models.CharField(max_length=16)
    template_suffix = models.CharField(max_length=32, null=True)
    title = models.CharField(max_length=255)
    updated_at = models.DateTimeField()

    class Meta:
        app_label = "shopify_sync"

    @property
    def collects(self) -> QueryType[Collect]:
        """
        Property of CustomCollection, returns related collect objects
        :return: Queryset
        :rtype: QueryType[Collect]
        """
        return Collect.objects.filter(self.user, collection_id=self.id)
        # todo where is this user field coming from? wtf?
