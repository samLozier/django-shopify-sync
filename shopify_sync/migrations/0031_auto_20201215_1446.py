# Generated by Django 3.1 on 2020-12-15 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shopify_sync", "0030_auto_20201215_1313"),
    ]

    operations = [
        migrations.RenameField(
            model_name="variant",
            old_name="inventory_item_id",
            new_name="inventory_item",
        ),
    ]
