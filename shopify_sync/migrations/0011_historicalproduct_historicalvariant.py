# Generated by Django 3.1 on 2020-08-21 22:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shopify_sync", "0010_auto_20200819_1929"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalVariant",
            fields=[
                ("id", models.BigIntegerField(db_index=True)),
                ("admin_graphql_api_id", models.CharField(max_length=80)),
                ("created_at", models.DateTimeField(null=True)),
                ("updated_at", models.DateTimeField(null=True)),
                ("barcode", models.CharField(max_length=255, null=True)),
                (
                    "compare_at_price",
                    models.DecimalField(decimal_places=2, max_digits=10, null=True),
                ),
                (
                    "fulfillment_service",
                    models.CharField(default="manual", max_length=32),
                ),
                ("grams", models.IntegerField()),
                (
                    "inventory_management",
                    models.CharField(default="blank", max_length=32, null=True),
                ),
                (
                    "inventory_policy",
                    models.CharField(default="deny", max_length=32, null=True),
                ),
                ("inventory_quantity", models.IntegerField(null=True)),
                ("option1", models.CharField(max_length=255, null=True)),
                ("option2", models.CharField(max_length=255, null=True)),
                ("option3", models.CharField(max_length=255, null=True)),
                ("position", models.IntegerField(default=1, null=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("requires_shipping", models.BooleanField(default=True)),
                ("sku", models.CharField(max_length=255, null=True)),
                ("taxable", models.BooleanField(default=True)),
                ("title", models.CharField(blank=True, max_length=255, null=True)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField()),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="shopify_sync.product",
                    ),
                ),
                (
                    "session",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="shopify_sync.session",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical variant",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalProduct",
            fields=[
                ("id", models.BigIntegerField(db_index=True)),
                ("admin_graphql_api_id", models.CharField(max_length=80)),
                ("created_at", models.DateTimeField(null=True)),
                ("updated_at", models.DateTimeField(null=True)),
                ("body_html", models.TextField(default="", null=True)),
                ("handle", models.CharField(db_index=True, max_length=255)),
                ("product_type", models.CharField(db_index=True, max_length=255)),
                ("published_at", models.DateTimeField(null=True)),
                ("published_scope", models.CharField(default="global", max_length=64)),
                ("tags", models.CharField(blank=True, max_length=255)),
                ("template_suffix", models.CharField(max_length=255, null=True)),
                ("title", models.CharField(db_index=True, max_length=255)),
                ("vendor", models.CharField(db_index=True, max_length=255, null=True)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField()),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "session",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="shopify_sync.session",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical product",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
