# Generated by Django 3.1.1 on 2020-09-17 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mtn_web', '0010_auto_20200901_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='publishing_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='publishing_sources', to='mtn_web.country'),
        ),
        migrations.AlterField(
            model_name='source',
            name='readership_countries',
            field=models.ManyToManyField(related_name='readership_sources', to='mtn_web.Country'),
        ),
    ]
