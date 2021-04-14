from __future__ import unicode_literals

from typing import Union

import shopify
from django.core.serializers.json import DjangoJSONEncoder


def empty_list() -> list[str]:
    """
    WTF is the point of this?
    :return: generates, you guessed it, an empty list
    :rtype: list[str]
    """
    return []


class ShopifyDjangoJSONEncoder(DjangoJSONEncoder):
    """As per: https://docs.djangoproject.com/en/1.6/topics/serialization/,
    this is a special encoder that handles lazily evaluated strings."""

    def default(
        self, obj: Union[shopify.Receipt, shopify.ShopifyResource]
    ) -> Union[str, dict]:
        if isinstance(obj, shopify.Receipt):
            return str(obj)
        if isinstance(obj, shopify.ShopifyResource) and getattr(obj, "attributes"):
            return obj.attributes
        return super(ShopifyDjangoJSONEncoder, self).default(obj)
