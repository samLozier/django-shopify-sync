# Generated by Django 2.2.5 on 2019-09-18 15:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('shopify_sync', '0008_order_fulfillments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='body_html',
            field=models.TextField(default='', null=True),
        ),
    ]
