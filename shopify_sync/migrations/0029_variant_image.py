# Generated by Django 3.1 on 2020-11-25 23:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("shopify_sync", "0028_auto_20200910_0613"),
    ]

    operations = [
        migrations.AddField(
            model_name="variant",
            name="image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="shopify_sync.image",
            ),
        ),
    ]
