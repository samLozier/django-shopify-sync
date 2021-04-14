# Generated by Django 3.1 on 2020-08-24 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopify_sync", "0013_auto_20200824_2105"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shop",
            name="eligible_for_payments",
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name="shop",
            name="google_apps_login_enabled",
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name="shop",
            name="password_enabled",
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name="shop",
            name="public",
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name="shop",
            name="requires_extra_payments_agreement",
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name="shop",
            name="tax_shipping",
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name="shop",
            name="taxes_included",
            field=models.BooleanField(default=False, null=True),
        ),
    ]