# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopify_sync', '0008_auto_20160314_2331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='user',
        ),
        migrations.RemoveField(
            model_name='carrierservice',
            name='user',
        ),
        migrations.RemoveField(
            model_name='collect',
            name='user',
        ),
        migrations.RemoveField(
            model_name='customcollection',
            name='user',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.RemoveField(
            model_name='image',
            name='user',
        ),
        migrations.RemoveField(
            model_name='lineitem',
            name='user',
        ),
        migrations.RemoveField(
            model_name='metafield',
            name='user',
        ),
        migrations.RemoveField(
            model_name='option',
            name='user',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.RemoveField(
            model_name='product',
            name='user',
        ),
        migrations.RemoveField(
            model_name='scripttag',
            name='user',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='user',
        ),
        migrations.RemoveField(
            model_name='smartcollection',
            name='user',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='user',
        ),
        migrations.RemoveField(
            model_name='webhook',
            name='user',
        ),
    ]
