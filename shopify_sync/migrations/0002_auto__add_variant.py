# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Variant'
        db.create_table(u'shopify_sync_variant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['product_options_app.ProductOptionsAppUser'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('barcode', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('compare_at_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2)),
            ('fulfillment_service', self.gf('django.db.models.fields.CharField')(default='manual', max_length=32)),
            ('grams', self.gf('django.db.models.fields.IntegerField')()),
            ('inventory_management', self.gf('django.db.models.fields.CharField')(default='blank', max_length=32)),
            ('inventory_policy', self.gf('django.db.models.fields.CharField')(default='deny', max_length=32)),
            ('inventory_quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('option1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('option2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('option3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('product_id', self.gf('django.db.models.fields.IntegerField')()),
            ('requires_shipping', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sku', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('taxable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('shopify_sync', ['Variant'])


    def backwards(self, orm):
        # Deleting model 'Variant'
        db.delete_table(u'shopify_sync_variant')


    models = {
        'product_options_app.productoptionsappuser': {
            'Meta': {'object_name': 'ProductOptionsAppUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'myshopify_domain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'uninstalled'", 'max_length': '16'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'shopify_sync.collect': {
            'Meta': {'object_name': 'Collect'},
            'collection_id': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'product_id': ('django.db.models.fields.IntegerField', [], {}),
            'sort_value': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product_options_app.ProductOptionsAppUser']"})
        },
        'shopify_sync.customcollection': {
            'Meta': {'object_name': 'CustomCollection'},
            'body_html': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'published_scope': ('django.db.models.fields.CharField', [], {'default': "'global'", 'max_length': '16'}),
            'sort_order': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'template_suffix': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product_options_app.ProductOptionsAppUser']"})
        },
        'shopify_sync.product': {
            'Meta': {'object_name': 'Product'},
            'body_html': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'published_scope': ('django.db.models.fields.CharField', [], {'default': "'global'", 'max_length': '64'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'template_suffix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product_options_app.ProductOptionsAppUser']"}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'shopify_sync.scripttag': {
            'Meta': {'object_name': 'ScriptTag'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'src': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product_options_app.ProductOptionsAppUser']"})
        },
        'shopify_sync.shop': {
            'Meta': {'object_name': 'Shop'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'country_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'county_taxes': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'customer_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'eligible_for_payments': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'google_apps_domain': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'google_apps_login_enabled': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '4'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '4'}),
            'money_format': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'money_in_emails_format': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'money_with_currency_format': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'money_with_currency_in_emails_format': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'myshopify_domain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'password_enabled': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'plan_display_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'plan_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'primary_location_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'province_code': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'public': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'requires_extra_payments_agreement': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'shop_owner': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'tax_shipping': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'taxes_included': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product_options_app.ProductOptionsAppUser']"}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'})
        },
        'shopify_sync.smartcollection': {
            'Meta': {'object_name': 'SmartCollection'},
            'body_html': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'disjunctive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'published_scope': ('django.db.models.fields.CharField', [], {'default': "'global'", 'max_length': '16'}),
            'rules': ('jsonfield.fields.JSONField', [], {}),
            'sort_order': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'template_suffix': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product_options_app.ProductOptionsAppUser']"})
        },
        'shopify_sync.variant': {
            'Meta': {'object_name': 'Variant'},
            'barcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'compare_at_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fulfillment_service': ('django.db.models.fields.CharField', [], {'default': "'manual'", 'max_length': '32'}),
            'grams': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventory_management': ('django.db.models.fields.CharField', [], {'default': "'blank'", 'max_length': '32'}),
            'inventory_policy': ('django.db.models.fields.CharField', [], {'default': "'deny'", 'max_length': '32'}),
            'inventory_quantity': ('django.db.models.fields.IntegerField', [], {}),
            'option1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'option2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'option3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'product_id': ('django.db.models.fields.IntegerField', [], {}),
            'requires_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'taxable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product_options_app.ProductOptionsAppUser']"})
        },
        'shopify_sync.webhook': {
            'Meta': {'object_name': 'Webhook'},
            'address': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fields': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metafield_namespaces': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product_options_app.ProductOptionsAppUser']"})
        }
    }

    complete_apps = ['shopify_sync']