from __future__ import unicode_literals

from shopify_webhook.tests import WebhookTestCase
from datetime import datetime
from dateutil import parser
from decimal import Decimal


class SyncTestCase(WebhookTestCase):
    """
    Base class providing helpers for running synchronisation-based tests.
    """

    def assertSynced(self, session, data, model):
        """
        Check that the given data has been synchronised locally for the given user and model class.
        """

        instance = model.objects.get(id=data['id'], session=session)

        # Check all direct fields on the instance were synchronised across correctly.
        for field in model.get_default_fields():
            if field in data:
                expected_value = data[field]
                actual_value = getattr(instance, field)

                # If our value is a datetime, ensure expected value is a UTC datetime object too.
                if isinstance(actual_value, datetime):
                    expected_value = parser.parse(expected_value)
                    expected_value = expected_value.utctimetuple()
                    actual_value = actual_value.utctimetuple()

                # If our value is a Decimal, convert the expected value to Decimal.
                if isinstance(actual_value, Decimal):
                    expected_value = Decimal(expected_value)

                # Assert values are equal.
                if expected_value != actual_value:
                    print("Field '%s' expected value is '%s' not '%s'" % (field, expected_value, actual_value,))
                self.assertEqual(expected_value, actual_value)

        # Check all child fields on the instance were synchronised correctly.
        for child_field, child_model in model.get_child_fields().items():
            for child_data in data[child_field]:
                self.assertSynced(session, child_data, child_model)
