# Generated by Django 3.1 on 2020-09-01 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopify_sync', '0020_auto_20200901_2013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventorylevel',
            name='available',
        ),
    ]
