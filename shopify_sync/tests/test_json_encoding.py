from . import SyncTestCase
from ..models import Product
from .recipes import UserRecipe


class JSONEncodingTestCase(SyncTestCase):

    def test_json_encoding(self):
        # Create a test user.
        user = UserRecipe.make(id = 1, username = 'test.myshopify.com')

        # Load JSON from the fixture file.
        fixture_json = self.read_fixture('product_created')

        # Create a product model by synchronising from a JSON fixture.
        fixture_shopify_resource = Product.shopify_resource_from_json(fixture_json)
        local_instance = Product.objects.sync_one(user, fixture_shopify_resource)

        # Call the JSON conversion method.
        local_json = local_instance.to_json()

        # Remove the 'image' attribute in the fixture JSON if present, as it's not a 'real' attribute.
        if 'image' in fixture_json:
            del fixture_json['image']

        # Verify the converted version and the JSON fixture are the same.
        self.assertEqual(local_json, fixture_json, "Local JSON encoding produces same JSON as fixture.")
