from enum import Enum
from datetime import datetime
from typing import NoReturn
import pycountry
from django.conf import settings
from django.db import models




class QueryResultSet(models.Model):
    query_types         = ( ('headlines', 'Headlines'), ('all', 'All') )
    argument           = models.CharField(max_length=500)
    choropleth         = models.TextField(max_length=2000000, blank=True)
    choro_html         = models.TextField(max_length=200000, blank=True)
    data               = models.CharField(max_length=200000, blank=True)
    date_created       = models.DateField(auto_now_add=True)
    date_last_modified = models.DateField(default=None, null=True, blank=True)
    date_range_end     = models.DateField(default=None, null=True, blank=True)
    date_range_start   = models.DateField(default=None, null=True, blank=True)
    filename           = models.TextField(max_length=700, blank=True)
    filepath           = models.TextField(max_length=1000, blank=True)
    public             = models.BooleanField(default=False)
    query_type         = models.CharField(default='all', choices=query_types, max_length=50)
    author             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='queries')
    archived           = models.BooleanField(default=False)
    article_count      = models.IntegerField(default=0)
    article_data_len   = models.IntegerField(default=0)

    def __str__(self):
        details = f'Argument: {self.argument}\n Query Type: {self.query_type}\n Author: {self.author}\n Archived: {self.archived}\n' \
                  f'Public: {self.public}\n Data[:500]: {self.data[:500]}\n ChoroHTML: {self.choro_html[:500]}'
        if self.filename:
            details = f'{details}\nFilename = {self.filename}'
        return details

    @property
    def date_created_readable(self) -> str:
        return f'{self.date_created.month}, {self.date_created.day}, {self.date_created.year}'


class CategoryChoice(Enum):
    BIZ = 'Business'
    ENT = 'Entertainment'
    HLT = 'Health'
    SCI = 'Science'
    SPO = 'Sports'
    TEC = 'Technology'
    GEN = 'General'


class Category(models.Model):
    name = models.CharField(max_length=50, choices=[(tag, tag.value) for tag in CategoryChoice])


class Source(models.Model):
    name       = models.CharField(max_length=500)
    country    = models.CharField(max_length=3)
    language   = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category, related_name='sources')
    url        = models.URLField(blank=True, default='', max_length=150)
    verified   = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.name}, {self.country}, {self.country}'

    @property
    def country_full_name(self) -> str:
        try:
            return pycountry.countries.lookup(self.country).name
        except LookupError:
            return self.country

    @property
    def language_full_name(self) -> str:
        try:
            return pycountry.languages.lookup(self.language).name
        except LookupError:
            return self.language


class Article(models.Model):
    article_url    = models.URLField(max_length=1000)
    author         = models.CharField(max_length=150)
    date_published = models.DateTimeField()
    description    = models.CharField(max_length=2500)
    image_url      = models.URLField(max_length=1000, default=None, blank=True, null=True)
    query          = models.ForeignKey(QueryResultSet, on_delete=models.CASCADE, related_name='articles')
    source         = models.ForeignKey(Source, on_delete=models.PROTECT, related_name='articles')
    title          = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.title}, {self.author}, {self.date_published}, {self.source.name}'

    @property
    def source_country(self) -> str:
        return self.source.country


class Post(models.Model):
    title          = models.CharField(max_length=300, default='', null=True, blank=True)
    body           = models.CharField(max_length=50000, default='', null=True, blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    author         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='posts')
    date_last_edit = models.DateTimeField(auto_now_add=True)
    query          = models.OneToOneField(QueryResultSet, on_delete=models.PROTECT)
    public         = models.BooleanField(default=False)

    def get_choro_map(self) -> str or NoReturn:
        if self.query:
            qrs_pk = self.query.pk
            qrs = QueryResultSet.objects.get(qrs_pk)
            return qrs.choropleth if qrs.choropleth else None
        return None


class Comment(models.Model):
    post           = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='comments')
    body           = models.CharField(max_length=25000)
    date_published = models.DateTimeField(auto_now_add=True)
    date_last_edit = models.DateTimeField(auto_now_add=True)
    author         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='comments')

    def __str__(self) -> str:
        return f'Comment from {self.author.first_name} {self.author.last_name} on {self.date_published} to post "{self.post.title}", made {self.date_published}'


#======================================================================================#
# enum help from
#   https://hackernoon.com/using-enum-as-model-field-choice-in-django-92d8b97aaa63
