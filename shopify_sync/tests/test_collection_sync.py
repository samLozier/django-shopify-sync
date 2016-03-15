from . import SyncTestCase
from ..models import CustomCollection, SmartCollection
from .recipes import UserRecipe


class CollectionSyncTestCase(SyncTestCase):

    def test_smart_collection_created_on_create_webhook(self):
        # Create a test user.
        user = UserRecipe.make(id = 1, username = 'test.myshopify.com')

        # Send a test "collection created" webhook with a SmartCollection payload.
        data = self.read_fixture('smartcollection_created')
        self.post_shopify_webhook(topic = 'collections/create', domain = user.username, data = data)

        # Verify that the synchronisation occurred.
        self.assertSynced(user, data, SmartCollection)

    def test_custom_collection_created_on_create_webhook(self):
        # Create a test user.
        user = UserRecipe.make(id = 1, username = 'test.myshopify.com')

        # Send a test "collection created" webhook with a CustomCollection paylod.
        data = self.read_fixture('customcollection_created')
        self.post_shopify_webhook(topic = 'collections/create', domain = user.username, data = data)

        # Verify that the synchronisation occurred.
        self.assertSynced(user, data, CustomCollection)
