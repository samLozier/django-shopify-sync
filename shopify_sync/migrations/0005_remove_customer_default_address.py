# Generated by Django 2.2.2 on 2019-06-22 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopify_sync', '0004_auto_20190621_0852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='default_address',
        ),
    ]

