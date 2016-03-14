# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopify_sync', '0007_genericipfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='carrierservice',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='collect',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='customcollection',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='lineitem',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='metafield',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='option',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='scripttag',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='smartcollection',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='webhook',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
    ]
