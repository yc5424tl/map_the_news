# Generated by Django 3.1 on 2020-09-01 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mtn_web', '0006_country_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='publishing_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='publishers', to='mtn_web.country'),
        ),
        migrations.AlterField(
            model_name='source',
            name='name',
            field=models.CharField(max_length=500, unique=True),
        ),
    ]
