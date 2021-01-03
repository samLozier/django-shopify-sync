from __future__ import unicode_literals

import json

import shopify
from django.db import models
from jsonfield import JSONField
from pyactiveresource.connection import ResourceInvalid

from .base import ShopifyDatedResourceModel
from .customer import Customer
from .line_item import LineItem
from .session import activate_session
from ..encoders import ShopifyDjangoJSONEncoder, empty_list


class Order(ShopifyDatedResourceModel):
    shopify_resource_class = shopify.resources.Order
    related_fields = ['customer']
    r_fields = {
        'customer': Customer,
    }
    child_fields = {
        'line_items': LineItem,
    }

    billing_address = JSONField(null=True, dump_kwargs = {'cls': ShopifyDjangoJSONEncoder})
    browser_ip = models.GenericIPAddressField(null = True)
    buyer_accepts_marketing = models.BooleanField(default = False)
    cancel_reason = models.CharField(max_length = 32, null = True)
    cancelled_at = models.DateTimeField(null = True)
    cart_token = models.CharField(max_length = 32, null = True)
    client_details = JSONField(dump_kwargs = {'cls': ShopifyDjangoJSONEncoder}, null=True)
    closed_at = models.DateTimeField(null = True)
    currency = models.CharField(max_length = 3)
    customer = models.ForeignKey('shopify_sync.Customer', null=True, on_delete=models.CASCADE)
    discount_codes = JSONField(default = empty_list, dump_kwargs = {'cls': ShopifyDjangoJSONEncoder}, null=True)
    email = models.EmailField()
    financial_status = models.CharField(max_length = 32)
    fulfillment_status = models.CharField(max_length = 32, null = True)
    fulfillments = JSONField(default=empty_list, dump_kwargs={'cls': ShopifyDjangoJSONEncoder}, null=True)
    tags = models.TextField(null=True)
    landing_site = models.URLField(max_length=2048, null=True)
    name = models.CharField(max_length = 32)
    note = models.TextField(null = True)
    note_attributes = JSONField(dump_kwargs = {'cls': ShopifyDjangoJSONEncoder}, null=True)
    number = models.IntegerField()
    order_number = models.BigIntegerField()
    processed_at = models.DateTimeField()
    processing_method = models.CharField(max_length = 32)
    referring_site = models.URLField(max_length = 2048, null = True)
    shipping_address = JSONField(null=True, dump_kwargs = {'cls': ShopifyDjangoJSONEncoder})
    shipping_lines = JSONField(default = empty_list, dump_kwargs = {'cls': ShopifyDjangoJSONEncoder})
    source_name = models.CharField(max_length = 32)
    tax_lines = JSONField(default = empty_list, dump_kwargs = {'cls': ShopifyDjangoJSONEncoder}, null=True)
    taxes_included = models.BooleanField(default = True)
    token = models.CharField(max_length = 32)
    total_discounts = models.DecimalField(max_digits = 10, decimal_places = 2)
    total_line_items_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    total_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    total_tax = models.DecimalField(max_digits = 10, decimal_places = 2)
    total_weight = models.DecimalField(max_digits = 10, decimal_places = 2)

    class Meta:
        app_label = 'shopify_sync'

    def fix_ids(self):
        for line_item in self.line_items:
            line_item.fix_ids()

    def _line_items(self):
        return LineItem.objects.filter(order=self)
    line_items = property(_line_items)

    def calculate_refund(self, line_items=None):
        URL = 'refunds/calculate'
        line_items = line_items if line_items else self.line_items
        refund_lines = []
        for line in line_items:
            refund_lines.append({
                "line_item_id": line.id,
                "quantity": line.quantity
            })

        data = {
            "refund": {
               "shipping": {
                    "full_refund": True
                },
                "refund_line_items": refund_lines
            }
        }
        body = json.dumps(data)
        with activate_session(self) as shopify_resource:
            try:
                response = shopify_resource.post(URL, body=body)
            except ResourceInvalid as response:
                return response

        body = json.loads(response.body)
        errors = data.pop('errors', None)
        if errors:
            return errors
        return body

    def refund_from_transaction(self, data):
        URL = 'refunds'

        errors = data.pop('errors', None)
        if errors:
            return errors

        transactions = data['refund'].pop('transactions')
        if not transactions:
            return "could not refund"
        for transaction in transactions:
            transaction.update({
                "kind": "refund",
            })
        data['refund'].update({
            "restock": False,
            "note": "The Campaign failed, sorry",
            "transactions": transactions,
        })

        body = json.dumps(data)
        with activate_session(self) as shopify_resource:
            response = shopify_resource.post(URL, body=body)
        body = json.loads(response.body)

        return body

    def refund(self, **kwargs):
        data = self.calculate_refund(**kwargs)
        if isinstance(data, dict):
            return self.refund_from_transaction(data)
        else:
            return data

    def _refunds(self):
        URL = "refunds"
        with activate_session(self) as shopify_resource:
            return shopify_resource.get(URL)
    refunds = property(_refunds)

    def __str__(self):
        return self.name
