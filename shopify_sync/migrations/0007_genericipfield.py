# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopify_sync', '0006_auto_20160314_0532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='browser_ip',
            field=models.GenericIPAddressField(null=True),
        ),
    ]
