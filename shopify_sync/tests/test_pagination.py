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
            'pagination_1',
            url='https://test.myshopify.com/admin/api/2020-01/shopify_foos.json?limit=2',
            method='GET',
            headers={'X-shopify-access-token': 'test'},
            body='{"products": [{ "id": 1 },{ "id": 2 }]}',
            response_headers={
                'Link': '<https://test.myshopify.com/admin/api/2020-01/shopify_foos.json?limit=2&page_info=abcde1>; rel="next"'
            }
        )

        self.fake(
            'pagination_2',
            url='https://test.myshopify.com/admin/api/2020-01/shopify_foos.json?limit=2&page_info=abcde1',
            method='GET',
            headers={'X-shopify-access-token': 'test'},
            body='{"products": [{ "id": 3 },{ "id": 4 }]}',
            response_headers={
                'Link': '<https://test.myshopify.com/admin/api/2020-01/shopify_foos.json?limit=2&page_info=abcde2>; rel="next"'
            }
        )

        self.fake(
            'pagination_3',
            url='https://test.myshopify.com/admin/api/2020-01/shopify_foos.json?limit=2&page_info=abcde2',
            method='GET',
            headers={'X-shopify-access-token': 'test'},
            body='{"products": [{ "id": 5 }]}',
        )
 
        count = 0

        for thing in manager.fetch_all(session, limit=2):
            count += 1
        
        self.assertEqual(count, 5)
