# Generated by Django 3.1 on 2020-12-23 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shopify_sync", "0035_auto_20201223_0937"),
    ]

    operations = [
        migrations.RenameField(
            model_name="variant",
            old_name="inventoryitem",
            new_name="inventory_item_id",
        ),
    ]
