# Generated by Django 4.0.2 on 2022-03-23 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chhapai', '0023_ordertype_jobs_order_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='order_type',
        ),
    ]