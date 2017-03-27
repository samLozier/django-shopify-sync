from . import SyncTestCase
from ..models import Product
from .recipes import SessionRecipe


class ProductSyncTestCase(SyncTestCase):

    def test_product_created_on_create_webhook(self):
        # Create a test user.
        session = SessionRecipe.make(id=1)

        # Send a test "product created" webhook.
        data = self.read_fixture('product_created')
        response = self.post_shopify_webhook(topic='products/create', domain=session.site, data=data)

        # Verify that the synchronisation occurred.
        self.assertEqual(response.status_code, 200)
        print(Product.objects.all())
        self.assertSynced(session, data, Product)
