# Generated by Django 4.0.2 on 2022-03-09 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chhapai', '0019_alter_jobs_job_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='billing_address',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
