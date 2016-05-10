import logging

import shopify
from django.conf import settings
from shopify_sync import models

shop_url = ("https://%s:%s@%s.myshopify.com/admin" %
            (settings.SHOPIFY_API_KEY,
             settings.SHOPIFY_PASSWORD,
             settings.SHOP_NAME, ))
shopify.ShopifyResource.set_site(shop_url)
log = logging.getLogger(__name__)


def pull(Model, *args, **kwargs):
    try:
        Model = getattr(models, Model)
        ShopifyModel = getattr(shopify, Model)
    except AttributeError:
        raise NotImplementedError
    objs = []
    caller = kwargs.get('caller', None)
    pages = kwargs.get('pages', 0)
    if caller:
        stdout = caller.stdout
    else:
        from sys import stdout
    pages = pages + 1 if pages else 0
    stdout.write("Grabing %s from Shopify...\n" % Model.__name__)
    total = (ShopifyModel.count() // 250) + 2  # 1 to round up, one beccause it is not 0-indexed
    for i in range(1, pages or total):
        stdout.write("\tGetting page %i/%i\n" % (i, (pages or total) - 1,))
        objs += ShopifyModel.find(query='', limit=250, page=i)
    stdout.write("%i %s are in Shopify\n" % (total, Model.__name__))
    count = {'count': 0, 'model': Model.__name__}
    for obj in objs:
        Model.objects.create(**obj)
        count['count'] += 1
        stdout.write('\tAdded/Updated %s %i\n' % (Model.__name__, obj.attributes['id'],))
    stdout.write('Added/updated %(count)i %(model)ss.' % count)
