# Generated by Django 3.0.6 on 2020-05-27 05:29

from django.db import migrations, models
import mtn_web.models


class Migration(migrations.Migration):

    dependencies = [
        ('mtn_web', '0002_auto_20200526_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='query_type',
            field=models.CharField(choices=[(mtn_web.models.QueryTypeChoice['HDL'], 'Headlines'), (mtn_web.models.QueryTypeChoice['ALL'], 'All')], default=mtn_web.models.QueryTypeChoice['ALL'], max_length=50),
        ),
    ]
