# Generated by Django 3.1 on 2020-09-01 16:35

import django.db.models.deletion
from django.db import migrations, models

import shopify_sync.models.base


class Migration(migrations.Migration):

    dependencies = [
        ("shopify_sync", "0015_variant_inventory_item_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="InventoryItem",
            fields=[
                ("admin_graphql_api_id", models.CharField(max_length=80)),
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                (
                    "cost",
                    models.DecimalField(decimal_places=2, max_digits=10, null=True),
                ),
                (
                    "country_code_of_origin",
                    models.CharField(blank=True, max_length=2, null=True),
                ),
                (
                    "country_harmonized_system_codes",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("created_at", models.DateTimeField(null=True)),
                (
                    "harmonized_system_code",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "province_code_of_origin",
                    models.CharField(blank=True, max_length=2, null=True),
                ),
                ("sku", models.CharField(max_length=255, null=True)),
                ("tracked", models.BooleanField(default=True, null=True)),
                ("updated_at", models.DateTimeField(null=True)),
                ("requires_shipping", models.BooleanField(default=True, null=True)),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shopify_sync.session",
                    ),
                ),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
        migrations.CreateModel(
            name="InventoryLevel",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("admin_graphql_api_id", models.CharField(max_length=80)),
                ("created_at", models.DateTimeField(null=True)),
                ("location_id", models.IntegerField(db_index=True, null=True)),
                ("updated_at", models.DateTimeField(null=True)),
                ("available", models.IntegerField(default=0, null=True)),
                (
                    "inventory_item_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shopify_sync.inventoryitem",
                    ),
                ),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shopify_sync.session",
                    ),
                ),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
    ]