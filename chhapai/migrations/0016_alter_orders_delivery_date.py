# Generated by Django 4.0.2 on 2022-06-27 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chhapai', '0015_orders_discount_orders_shipping_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
