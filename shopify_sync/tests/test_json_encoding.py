from __future__ import unicode_literals

from unittest import mock

from . import SyncTestCase
from ..models import Product
from .recipes import SessionRecipe
from pprint import pformat


class JSONEncodingTestCase(SyncTestCase):

    @mock.patch('shopify.resources.Metafield.find')
    def test_json_encoding(self, mock_find):
        # Create a test user.
        session = SessionRecipe.make(id=1)

        # Load JSON from the fixture file.
        fixture_json = self.read_fixture('product_created')

        # Create a product model by synchronising from a JSON fixture.
        fixture_shopify_resource = Product.shopify_resource_from_json(fixture_json)
        fixture_shopify_resource.session = session
        local_instance = Product.objects.sync_one(fixture_shopify_resource)

        # Call the JSON conversion method.
        local_json = local_instance.to_json()

        # Remove the 'image' attribute in the fixture JSON if present, as it's not a 'real' attribute.
        if 'image' in fixture_json:
            del fixture_json['image']

        # remove session from json
        if 'session' in fixture_json:
            del fixture_json['session']

        # Verify the converted version and the JSON fixture are the same.
        string = """Local JSON encoding produces same JSON as fixture.
fixture json
%s
================
Local json
%s
""" % (
            pformat(fixture_json),
            pformat(local_json),
        )
        self.assertEqual(local_json, fixture_json, msg=string)


