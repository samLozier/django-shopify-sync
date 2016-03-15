from . import SyncTestCase
from ..models import Product
from .recipes import UserRecipe


class ProductSyncTestCase(SyncTestCase):

    def test_product_created_on_create_webhook(self):
        # Create a test user.
        user = UserRecipe.make(id = 1, username = 'test.myshopify.com')

        # Send a test "product created" webhook.
        data = self.read_fixture('product_created')
        self.post_shopify_webhook(topic = 'products/create', domain = user.username, data = data)

        # Verify that the synchronisation occurred.
        self.assertSynced(user, data, Product)
