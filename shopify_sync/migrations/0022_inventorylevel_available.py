# Generated by Django 3.1 on 2020-09-01 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopify_sync", "0021_remove_inventorylevel_available"),
    ]

    operations = [
        migrations.AddField(
            model_name="inventorylevel",
            name="available",
            field=models.IntegerField(default=0, null=True),
        ),
    ]