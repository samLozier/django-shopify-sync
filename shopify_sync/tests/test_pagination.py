from shopify_sync.models.base import ShopifyResourceManager
from shopify_sync.models import Session
from .test_helpers import TestCase
import shopify


class ShopifyFoo(shopify.base.ShopifyResource):
    pass


class FooModel():
    shopify_resource_class = ShopifyFoo


class PaginationCase(TestCase):
    def test_shopify_sync_pagination(self):
        manager = ShopifyResourceManager()
        manager.model = FooModel
        session = Session.objects.create(token="test", site="test")
        self.fake(
            'shop',
            url='https://test.myshopify.com/admin/shop.json',
            method='GET',
            body='lol!',
            headers={'Authorization': u'Basic dXNlcjpwYXNz'}
        )
        for thing in manager.fetch_all(session, limit=2):
            print(thing)