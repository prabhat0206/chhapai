# Generated by Django 4.0.2 on 2022-04-02 07:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chhapai', '0002_alter_midorder_stage_delete_stages'),
    ]

    operations = [
        migrations.AddField(
            model_name='challans',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='challans',
            name='dispatch_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='challans',
            name='no_of_packs',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='challans',
            name='quantity_per_pack',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='payments',
            name='payment_method',
            field=models.CharField(default='Cash', max_length=255),
        ),
        migrations.AddField(
            model_name='payments',
            name='payment_note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
