# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopify_sync', '0005_auto_20150505_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrierservice',
            name='carrier_service_type',
            field=models.CharField(default='api', choices=[('api', 'API'), ('legacy', 'Legacy')], max_length=16),
        ),
        migrations.AlterField(
            model_name='customcollection',
            name='published_scope',
            field=models.CharField(default='global', max_length=16),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='metafield',
            name='owner_resource',
            field=models.CharField(default='shop', choices=[('shop', 'Shop'), ('product', 'Product')], max_length=32),
        ),
        migrations.AlterField(
            model_name='metafield',
            name='value_type',
            field=models.CharField(default='string', choices=[('string', 'String'), ('integer', 'Integer')], max_length=32),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='product',
            name='published_scope',
            field=models.CharField(default='global', max_length=64),
        ),
        migrations.AlterField(
            model_name='shop',
            name='customer_email',
            field=models.EmailField(null=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='shop',
            name='email',
            field=models.EmailField(null=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='smartcollection',
            name='published_scope',
            field=models.CharField(default='global', max_length=16),
        ),
        migrations.AlterField(
            model_name='variant',
            name='fulfillment_service',
            field=models.CharField(default='manual', max_length=32),
        ),
        migrations.AlterField(
            model_name='variant',
            name='inventory_management',
            field=models.CharField(default='blank', null=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='variant',
            name='inventory_policy',
            field=models.CharField(default='deny', null=True, max_length=32),
        ),
    ]
