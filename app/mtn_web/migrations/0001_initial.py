# Generated by Django 3.0.8 on 2020-07-30 05:08

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mtn_web.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
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
                ('choropleth', models.TextField(blank=True, max_length=2000000, null=True)),
                ('choro_html', models.TextField(blank=True, max_length=200000, null=True)),
                ('data', models.CharField(blank=True, default='', max_length=200000)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_last_modified', models.DateField(blank=True, default=None, null=True)),
                ('date_range_end', models.DateField(blank=True, default=None, null=True)),
                ('date_range_start', models.DateField(blank=True, default=None, null=True)),
                ('filename', models.TextField(blank=True, max_length=700, null=True)),
                ('filepath', models.TextField(blank=True, max_length=1000, null=True)),
                ('public', models.BooleanField(default=False)),
                ('query_type', models.CharField(choices=[(mtn_web.models.QueryTypeChoice['HDL'], 'Headlines'), (mtn_web.models.QueryTypeChoice['ALL'], 'All')], default=mtn_web.models.QueryTypeChoice['ALL'], max_length=50)),
                ('archived', models.BooleanField(default=False)),
                ('article_count', models.IntegerField(default=0)),
                ('article_data_len', models.IntegerField(default=0)),
                ('articles_per_country', django.contrib.postgres.fields.jsonb.JSONField(blank=True, max_length=20000, null=True)),
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