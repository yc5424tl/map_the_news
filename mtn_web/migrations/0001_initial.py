# Generated by Django 3.0.6 on 2020-05-17 03:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mtn_web.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('BIZ', 'business'), ('ENT', 'entertainment'), ('GEN', 'general'), ('HLT', 'health'), ('SCI', 'science'), ('SPO', 'sports'), ('TEC', 'technology')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('country', models.CharField(max_length=3)),
                ('language', models.CharField(max_length=100)),
                ('url', models.URLField(blank=True, default='', max_length=150)),
                ('verified', models.BooleanField(default=False)),
                ('categories', models.ManyToManyField(related_name='sources', to='mtn_web.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('argument', models.CharField(max_length=500)),
                ('choropleth', models.TextField(blank=True, max_length=2000000)),
                ('choro_html', models.TextField(blank=True, max_length=200000)),
                ('data', models.CharField(blank=True, max_length=200000)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_last_modified', models.DateField(blank=True, default=None, null=True)),
                ('date_range_end', models.DateField(blank=True, default=None, null=True)),
                ('date_range_start', models.DateField(blank=True, default=None, null=True)),
                ('filename', models.TextField(blank=True, max_length=700)),
                ('filepath', models.TextField(blank=True, max_length=1000)),
                ('public', models.BooleanField(default=False)),
                ('query_type', models.CharField(choices=[(mtn_web.models.QueryTypeChoice['HDL'], 'headlines'), (mtn_web.models.QueryTypeChoice['ALL'], 'all')], default=mtn_web.models.QueryTypeChoice['ALL'], max_length=50)),
                ('archived', models.BooleanField(default=False)),
                ('article_count', models.IntegerField(default=0)),
                ('article_data_len', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='results', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('body', models.CharField(blank=True, default='', max_length=50000, null=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('date_last_edit', models.DateTimeField(auto_now_add=True)),
                ('public', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('result', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='mtn_web.Result')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=25000)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('date_last_edit', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comments', to='mtn_web.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_url', models.URLField(max_length=1000)),
                ('author', models.CharField(max_length=150)),
                ('date_published', models.DateTimeField(blank=True, default=None, null=True)),
                ('description', models.CharField(max_length=2500)),
                ('image_url', models.URLField(blank=True, default=None, max_length=1000, null=True)),
                ('title', models.CharField(max_length=300)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', related_query_name='article', to='mtn_web.Result')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='articles', related_query_name='article', to='mtn_web.Source')),
            ],
        ),
    ]
