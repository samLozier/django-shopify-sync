# Generated by Django 3.1 on 2020-12-24 01:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopify_sync', '0039_variant_inventory_item_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='inventorylevel',
            unique_together={('inventory_item', 'location', 'id')},
        ),
    ]
