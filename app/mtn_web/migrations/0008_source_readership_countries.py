# Generated by Django 3.1 on 2020-09-01 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mtn_web', '0007_auto_20200901_0434'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='readership_countries',
            field=models.ManyToManyField(related_name='markets', to='mtn_web.Country'),
        ),
    ]
