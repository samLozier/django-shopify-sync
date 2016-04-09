# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopify_sync', '0009_auto_20160314_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collect',
            name='collection_id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='collect',
            name='product_id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_order_id',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='lineitem',
            name='product_id',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='lineitem',
            name='variant_id',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='metafield',
            name='owner_id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.BigIntegerField(),
        ),
    ]
