# Generated by Django 4.0.2 on 2022-04-04 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chhapai', '0006_alter_challans_order_alter_payments_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobs',
            name='isCompleted',
        ),
        migrations.AddField(
            model_name='jobs',
            name='amount_paid',
            field=models.IntegerField(default=0),
        ),
    ]
