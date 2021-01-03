# Generated by Django 2.1.4 on 2018-12-14 16:41

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import shopify_sync.encoders
import shopify_sync.models.base
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                ("address1", models.CharField(max_length=256, null=True)),
                ("address2", models.CharField(max_length=256, null=True)),
                ("city", models.CharField(max_length=256, null=True)),
                ("company", models.CharField(max_length=256, null=True)),
                ("country", models.CharField(max_length=256, null=True)),
                ("country_code", models.CharField(max_length=256, null=True)),
                ("country_name", models.CharField(max_length=256, null=True)),
                ("default", models.BooleanField(default=False)),
                ("first_name", models.CharField(max_length=256, null=True)),
                ("last_name", models.CharField(max_length=256, null=True)),
                ("phone", models.CharField(max_length=32, null=True)),
                ("province", models.CharField(max_length=32, null=True)),
                ("province_code", models.CharField(max_length=32, null=True)),
                ("zip", models.CharField(max_length=32, null=True)),
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
        migrations.CreateModel(
            name="CarrierService",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("active", models.BooleanField(default=True)),
                ("callback_url", models.URLField()),
                (
                    "carrier_service_type",
                    models.CharField(
                        choices=[("api", "API"), ("legacy", "Legacy")],
                        default="api",
                        max_length=16,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("service_discovery", models.BooleanField(default=True)),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
        migrations.CreateModel(
            name="Collect",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(null=True)),
                ("updated_at", models.DateTimeField(null=True)),
                ("collection_id", models.BigIntegerField()),
                ("featured", models.BooleanField(default=False)),
                ("position", models.IntegerField(default=1, null=True)),
                ("product_id", models.BigIntegerField()),
                ("sort_value", models.CharField(max_length=16, null=True)),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
        migrations.CreateModel(
            name="CustomCollection",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("body_html", models.TextField(null=True)),
                ("handle", models.CharField(max_length=255)),
                ("image", jsonfield.fields.JSONField(null=True)),
                ("published", models.BooleanField(default=True)),
                ("published_at", models.DateTimeField(null=True)),
                ("published_scope", models.CharField(default="global", max_length=16)),
                ("sort_order", models.CharField(max_length=16)),
                ("template_suffix", models.CharField(max_length=32, null=True)),
                ("title", models.CharField(max_length=255)),
                ("updated_at", models.DateTimeField()),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(null=True)),
                ("updated_at", models.DateTimeField(null=True)),
                ("accepts_marketing", models.BooleanField(default=False)),
                ("email", models.EmailField(max_length=254, null=True)),
                ("first_name", models.CharField(max_length=128, null=True)),
                ("multipass_identified", models.CharField(max_length=128, null=True)),
                ("last_name", models.CharField(max_length=128, null=True)),
                ("last_order_id", models.BigIntegerField(null=True)),
                ("last_order_name", models.CharField(max_length=128, null=True)),
                ("note", models.TextField(null=True)),
                ("orders_count", models.IntegerField()),
                ("state", models.CharField(max_length=32)),
                ("tags", models.TextField()),
                ("total_spent", models.DecimalField(decimal_places=2, max_digits=10)),
                ("verified_email", models.BooleanField(default=False)),
                (
                    "default_address",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="default_address",
                        to="shopify_sync.Address",
                    ),
                ),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(null=True)),
                ("updated_at", models.DateTimeField(null=True)),
                ("position", models.IntegerField(default=1, null=True)),
                ("src", models.URLField()),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
        migrations.CreateModel(
            name="LineItem",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("fulfillable_quantity", models.IntegerField()),
                ("fulfillment_service", models.CharField(max_length=32)),
                ("fulfillment_status", models.CharField(max_length=32, null=True)),
                ("grams", models.DecimalField(decimal_places=2, max_digits=10)),
                ("name", models.CharField(max_length=256)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("product_id", models.BigIntegerField(null=True)),
                ("product_exists", models.BooleanField(default=True)),
                (
                    "properties",
                    jsonfield.fields.JSONField(
                        default=shopify_sync.encoders.empty_list
                    ),
                ),
                ("quantity", models.IntegerField()),
                ("requires_shipping", models.BooleanField(default=True)),
                ("sku", models.CharField(max_length=256)),
                ("gift_card", models.BooleanField(default=False)),
                ("taxable", models.BooleanField(default=False)),
                (
                    "tax_lines",
                    jsonfield.fields.JSONField(
                        default=shopify_sync.encoders.empty_list
                    ),
                ),
                ("title", models.CharField(max_length=256)),
                (
                    "total_discount",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("variant_id", models.BigIntegerField(null=True)),
                ("variant_title", models.CharField(max_length=256, null=True)),
                ("vendor", models.CharField(max_length=64, null=True)),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
        migrations.CreateModel(
            name="Metafield",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(null=True)),
                ("updated_at", models.DateTimeField(null=True)),
                ("description", models.CharField(max_length=255, null=True)),
                ("key", models.CharField(max_length=30)),
                ("namespace", models.CharField(max_length=20)),
                ("owner_id", models.BigIntegerField()),
                (
                    "owner_resource",
                    models.CharField(
                        choices=[("shop", "Shop"), ("product", "Product")],
                        default="shop",
                        max_length=32,
                    ),
                ),
                ("value", models.TextField()),
                (
                    "value_type",
                    models.CharField(
                        choices=[("string", "String"), ("integer", "Integer")],
                        default="string",
                        max_length=32,
                    ),
                ),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
        migrations.CreateModel(
            name="Option",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("position", models.IntegerField(default=1, null=True)),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(null=True)),
                ("updated_at", models.DateTimeField(null=True)),
                ("billing_address", jsonfield.fields.JSONField(null=True)),
                ("browser_ip", models.GenericIPAddressField(null=True)),
                ("buyer_accepts_marketing", models.BooleanField(default=False)),
                ("cancel_reason", models.CharField(max_length=32, null=True)),
                ("cancelled_at", models.DateTimeField(null=True)),
                ("cart_token", models.CharField(max_length=32, null=True)),
                ("client_details", jsonfield.fields.JSONField(null=True)),
                ("closed_at", models.DateTimeField(null=True)),
                ("currency", models.CharField(max_length=3)),
                (
                    "discount_codes",
                    jsonfield.fields.JSONField(
                        default=shopify_sync.encoders.empty_list, null=True
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                ("financial_status", models.CharField(max_length=32)),
                ("fulfillment_status", models.CharField(max_length=32, null=True)),
                ("tags", models.TextField(null=True)),
                ("landing_site", models.URLField(max_length=2048, null=True)),
                ("name", models.CharField(max_length=32)),
                ("note", models.TextField(null=True)),
                ("note_attributes", jsonfield.fields.JSONField(null=True)),
                ("number", models.IntegerField()),
                ("order_number", models.BigIntegerField()),
                ("processed_at", models.DateTimeField()),
                ("processing_method", models.CharField(max_length=32)),
                ("referring_site", models.URLField(max_length=2048, null=True)),
                (
                    "shipping_lines",
                    jsonfield.fields.JSONField(
                        default=shopify_sync.encoders.empty_list
                    ),
                ),
                ("source_name", models.CharField(max_length=32)),
                (
                    "tax_lines",
                    jsonfield.fields.JSONField(
                        default=shopify_sync.encoders.empty_list, null=True
                    ),
                ),
                ("taxes_included", models.BooleanField(default=True)),
                ("token", models.CharField(max_length=32)),
                (
                    "total_discounts",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "total_line_items_price",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("total_tax", models.DecimalField(decimal_places=2, max_digits=10)),
                ("total_weight", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "customer",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shopify_sync.Customer",
                    ),
                ),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(null=True)),
                ("updated_at", models.DateTimeField(null=True)),
                ("body_html", models.TextField()),
                ("handle", models.CharField(db_index=True, max_length=255)),
                ("product_type", models.CharField(db_index=True, max_length=255)),
                ("published_at", models.DateTimeField(null=True)),
                ("published_scope", models.CharField(default="global", max_length=64)),
                ("tags", models.CharField(blank=True, max_length=255)),
                ("template_suffix", models.CharField(max_length=255, null=True)),
                ("title", models.CharField(db_index=True, max_length=255)),
                ("vendor", models.CharField(db_index=True, max_length=255, null=True)),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
        migrations.CreateModel(
            name="ScriptTag",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(null=True)),
                ("updated_at", models.DateTimeField(null=True)),
                ("event", models.CharField(max_length=16)),
                ("src", models.URLField()),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("token", models.CharField(max_length=255)),
                ("site", models.CharField(max_length=511)),
            ],
        ),
        migrations.CreateModel(
            name="ShippingAddress",
            fields=[
                ("address1", models.CharField(max_length=256, null=True)),
                ("address2", models.CharField(max_length=256, null=True)),
                ("city", models.CharField(max_length=256, null=True)),
                ("company", models.CharField(max_length=256, null=True)),
                ("country", models.CharField(max_length=256, null=True)),
                ("country_code", models.CharField(max_length=256, null=True)),
                ("country_name", models.CharField(max_length=256, null=True)),
                ("default", models.BooleanField(default=False)),
                ("first_name", models.CharField(max_length=256, null=True)),
                ("last_name", models.CharField(max_length=256, null=True)),
                ("phone", models.CharField(max_length=32, null=True)),
                ("province", models.CharField(max_length=32, null=True)),
                ("province_code", models.CharField(max_length=32, null=True)),
                ("zip", models.CharField(max_length=32, null=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
        migrations.CreateModel(
            name="Shop",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("myshopify_domain", models.CharField(max_length=255, unique=True)),
                ("domain", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255, null=True)),
                ("shop_owner", models.CharField(max_length=255, null=True)),
                ("email", models.EmailField(max_length=254, null=True)),
                ("customer_email", models.EmailField(max_length=254, null=True)),
                ("phone", models.CharField(max_length=32, null=True)),
                ("address1", models.CharField(max_length=255, null=True)),
                ("city", models.CharField(max_length=255, null=True)),
                ("zip", models.CharField(max_length=16, null=True)),
                ("province", models.CharField(max_length=255, null=True)),
                ("province_code", models.CharField(max_length=32, null=True)),
                ("country", models.CharField(max_length=255, null=True)),
                ("country_code", models.CharField(max_length=32, null=True)),
                ("country_name", models.CharField(max_length=255, null=True)),
                (
                    "latitude",
                    models.DecimalField(decimal_places=4, max_digits=7, null=True),
                ),
                (
                    "longitude",
                    models.DecimalField(decimal_places=4, max_digits=7, null=True),
                ),
                ("timezone", models.CharField(max_length=255, null=True)),
                ("currency", models.CharField(max_length=4, null=True)),
                ("money_format", models.CharField(max_length=32, null=True)),
                ("money_in_emails_format", models.CharField(max_length=32, null=True)),
                (
                    "money_with_currency_format",
                    models.CharField(max_length=32, null=True),
                ),
                (
                    "money_with_currency_in_emails_format",
                    models.CharField(max_length=32, null=True),
                ),
                ("county_taxes", models.NullBooleanField(default=False)),
                ("tax_shipping", models.NullBooleanField(default=False)),
                ("taxes_included", models.NullBooleanField(default=False)),
                ("google_apps_domain", models.CharField(max_length=255, null=True)),
                ("google_apps_login_enabled", models.NullBooleanField(default=False)),
                ("plan_name", models.CharField(max_length=32, null=True)),
                ("plan_display_name", models.CharField(max_length=32, null=True)),
                ("password_enabled", models.NullBooleanField(default=False)),
                ("primary_location_id", models.IntegerField(null=True)),
                ("public", models.NullBooleanField(default=True)),
                ("eligible_for_payments", models.NullBooleanField(default=True)),
                (
                    "requires_extra_payments_agreement",
                    models.NullBooleanField(default=True),
                ),
                ("source", models.CharField(max_length=32, null=True)),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shopify_sync.Session",
                    ),
                ),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
        migrations.CreateModel(
            name="SmartCollection",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("body_html", models.TextField(null=True)),
                ("handle", models.CharField(max_length=255)),
                ("image", jsonfield.fields.JSONField(null=True)),
                ("published_at", models.DateTimeField(null=True)),
                ("published_scope", models.CharField(default="global", max_length=16)),
                (
                    "rules",
                    jsonfield.fields.JSONField(
                        default=shopify_sync.encoders.empty_list
                    ),
                ),
                ("disjunctive", models.BooleanField(default=False)),
                ("sort_order", models.CharField(max_length=16)),
                ("template_suffix", models.CharField(max_length=32, null=True)),
                ("title", models.CharField(max_length=255)),
                ("updated_at", models.DateTimeField()),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shopify_sync.Session",
                    ),
                ),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
        migrations.CreateModel(
            name="Variant",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
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
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shopify_sync.Product",
                    ),
                ),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shopify_sync.Session",
                    ),
                ),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
        migrations.CreateModel(
            name="Webhook",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(null=True)),
                ("updated_at", models.DateTimeField(null=True)),
                ("topic", models.CharField(max_length=64)),
                ("address", models.URLField()),
                ("format", models.CharField(max_length=4)),
                ("fields", jsonfield.fields.JSONField(null=True)),
                ("metafield_namespaces", jsonfield.fields.JSONField(null=True)),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shopify_sync.Session",
                    ),
                ),
            ],
            bases=(shopify_sync.models.base.ChangedFields, models.Model),
        ),
        migrations.AddField(
            model_name="scripttag",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shopify_sync.Session"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shopify_sync.Session"
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shopify_sync.Session"
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="shipping_address",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shipping_address",
                to="shopify_sync.ShippingAddress",
            ),
        ),
        migrations.AddField(
            model_name="option",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shopify_sync.Product"
            ),
        ),
        migrations.AddField(
            model_name="option",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shopify_sync.Session"
            ),
        ),
        migrations.AddField(
            model_name="metafield",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="shopify_sync.Product",
            ),
        ),
        migrations.AddField(
            model_name="metafield",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shopify_sync.Session"
            ),
        ),
        migrations.AddField(
            model_name="lineitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shopify_sync.Order"
            ),
        ),
        migrations.AddField(
            model_name="lineitem",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shopify_sync.Session"
            ),
        ),
        migrations.AddField(
            model_name="image",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shopify_sync.Product"
            ),
        ),
        migrations.AddField(
            model_name="image",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shopify_sync.Session"
            ),
        ),
        migrations.AddField(
            model_name="customer",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shopify_sync.Session"
            ),
        ),
        migrations.AddField(
            model_name="customcollection",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shopify_sync.Session"
            ),
        ),
        migrations.AddField(
            model_name="collect",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shopify_sync.Session"
            ),
        ),
        migrations.AddField(
            model_name="carrierservice",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shopify_sync.Session"
            ),
        ),
    ]
