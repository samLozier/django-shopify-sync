from . import SyncTestCase
from ..models import CustomCollection, SmartCollection
from .recipes import SessionRecipe


class CollectionSyncTestCase(SyncTestCase):

    def test_smart_collection_created_on_create_webhook(self):
        # Create a test user.
        session = SessionRecipe.make(id=1)

        # Send a test "collection created" webhook with a SmartCollection payload.
        data = self.read_fixture('smartcollection_created')
        response = self.post_shopify_webhook(topic='collections/create', domain=session.site, data=data)

        # Verify that the synchronisation occurred.
        self.assertEqual(response.status_code, 200)
        # self.assertSynced(session, data, SmartCollection)

    def test_custom_collection_created_on_create_webhook(self):
        # Create a test user.
        session = SessionRecipe.make(id=1)

        # Send a test "collection created" webhook with a CustomCollection paylod.
        data = self.read_fixture('customcollection_created')
        response = self.post_shopify_webhook(topic='collections/create', domain=session.site, data=data)

        # Verify that the synchronisation occurred.
        self.assertEqual(response.status_code, 200)
        # self.assertSynced(session, data, CustomCollection)
