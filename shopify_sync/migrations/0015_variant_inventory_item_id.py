# Generated by Django 3.1 on 2020-09-01 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopify_sync', '0014_auto_20200824_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='inventory_item_id',
            field=models.IntegerField(db_index=True, null=True),
        ),
    ]
