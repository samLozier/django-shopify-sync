# Generated by Django 3.1 on 2020-09-01 17:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopify_sync", "0017_auto_20200901_1714"),
    ]

    operations = [
        migrations.RemoveField(model_name="variant", name="inventory_item_id",),
        migrations.AddField(
            model_name="inventoryitem",
            name="variant",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to="shopify_sync.variant",
            ),
            preserve_default=False,
        ),
    ]
