# Generated by Django 3.1 on 2020-09-10 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopify_sync", "0027_remove_variant_inventory_item_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lineitem",
            name="sku",
            field=models.CharField(max_length=256, null=True),
        ),
    ]
