# Generated by Django 3.1 on 2020-09-01 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopify_sync', '0019_auto_20200901_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryitem',
            name='variant',
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='variant_id',
            field=models.IntegerField(db_index=True, default=0),
            preserve_default=False,
        ),
    ]
