# Generated by Django 3.1 on 2021-01-30 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopify_sync", "0040_auto_20201223_1718"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="tags",
            field=models.CharField(blank=True, max_length=600),
        ),
    ]
