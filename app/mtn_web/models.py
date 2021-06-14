from enum import Enum
from typing import NoReturn

import pycountry
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import JSONField  # DO NOT import from 'django.contrib.postgres.fields'
from simple_history import register
from simple_history.models import HistoricalRecords


class QueryTypeChoice(Enum):
    HDL = "Headlines"
    ALL = "All"

    def __str__(self):
        return self.value


class Result(models.Model):
    argument = models.CharField(max_length=500)
    choropleth = models.TextField(max_length=2000000, blank=True, null=True)
    choro_html = models.TextField(max_length=200000, blank=True, null=True)
    data = models.CharField(max_length=200000, default="", blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_last_modified = models.DateField(default=None, null=True, blank=True)
    date_range_end = models.DateField(default=None, null=True, blank=True)
    date_range_start = models.DateField(default=None, null=True, blank=True)
    filename = models.TextField(max_length=700, blank=True, null=True)
    filepath = models.TextField(max_length=1000, blank=True, null=True)
    query_type = models.CharField(max_length=50, choices=[(tag, tag.value) for tag in QueryTypeChoice], default=QueryTypeChoice.ALL)
    author = models.ForeignKey("mtn_web.User", on_delete=models.PROTECT, related_name="results")
    archived = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    article_count = models.IntegerField(default=0)
    article_data_len = models.IntegerField(default=0)
    articles_per_country = JSONField(max_length=20000, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        details = (
            f"Argument: {self.argument}\nAuthor: {self.author}\nArchived: {self.archived}\n"
            f"Public: {self.public}\nData[:500]: {self.data[:500]}\nChoroHTML: {self.choro_html[:500]}"
        )
        if self.filename:
            details = f"{details}\nFilename = {self.filename}"
        return details

    @property
    def date_created_readable(self) -> str:
        return f"{self.date_created.month}, {self.date_created.day}, {self.date_created.year}"


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name.capitalize()

    def get_absolute_url(self):

        return f"/categories/{self.name}"


class Country(models.Model):
    alpha2_code = models.CharField(max_length=10, null=False, blank=False, default="--")
    display_name = models.CharField(max_length=100, blank=False, null=False, default="--")
    alphanum_name = models.CharField(max_length=100, blank=False, null=False, default="--")
    history = HistoricalRecords()

    class Meta:
        ordering = ["display_name"]

    def __str__(self):
        return f"{self.display_name} ({self.alpha2_code})"

    def get_absolute_url(self):
        return f"/countries/{self.alphanum_name}"


class Language(models.Model):
    alpha2_code = models.CharField(max_length=10, null=False, blank=False, default="--")
    display_name = models.CharField(max_length=100, blank=False, null=False, default="--")
    alphanum_name = models.CharField(max_length=100, blank=False, null=False, default="--")
    history = HistoricalRecords()

    class Meta:
        ordering = ["display_name"]

    def __str__(self):
        return f"{self.display_name} ({self.alpha2_code})"

    def get_absolute_url(self):
        return f"/languages/{self.alphanum_name}"


class Source(models.Model):

    country = models.CharField(max_length=3)
    language = models.CharField(max_length=100)

    name = models.CharField(max_length=500, unique=True)
    languages = models.ManyToManyField(Language, related_name="sources")
    publishing_country = models.ForeignKey("mtn_web.Country", on_delete=models.PROTECT, related_name="publishing_sources", null=True, blank=True)
    readership_countries = models.ManyToManyField(Country, related_name="readership_sources")
    categories = models.ManyToManyField(Category, related_name="sources")
    url = models.URLField(blank=True, default="", max_length=150)
    verified = models.BooleanField(default=False)

    country_alpha2_code = models.CharField(max_length=10, blank=False, null=False, default="alpha2code")
    country_display_name = models.CharField(max_length=100, blank=False, null=False, default="display_name_placeholder")
    country_alphanum_name = models.CharField(max_length=100, blank=False, null=False, default="alphanum_name_placeholder")

    language_alpha2_code = models.CharField(max_length=10, blank=False, null=False, default="alpha2code")
    language_display_name = models.CharField(max_length=100, blank=False, null=False, default="display_name_placeholder")
    language_alphanum_name = models.CharField(max_length=100, blank=False, null=False, default="alphanum_name_placeholder")

    history = HistoricalRecords()

    def __str__(self) -> str:
        return f"{self.name}"

    def get_absolute_url(self):
        return f"/sources/{self.name}/"


class Article(models.Model):
    article_url = models.URLField(max_length=1000)
    author = models.CharField(max_length=150)
    date_published = models.DateTimeField(default=None, null=True, blank=True)
    description = models.CharField(max_length=2500)
    image_url = models.URLField(max_length=1000, default=None, blank=True, null=True)
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name="articles", related_query_name="article",)
    source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name="articles", related_query_name="article",)
    title = models.CharField(max_length=300)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.title}, {self.author}, {self.date_published}, {self.source.name}"

    @property
    def source_country(self) -> str:
        return self.source.country


class Post(models.Model):
    title = models.CharField(max_length=300, default="", null=True, blank=True)
    body = models.CharField(max_length=50000, default="", null=True, blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("mtn_web.User", on_delete=models.PROTECT, related_name="posts")
    date_last_edit = models.DateTimeField(auto_now_add=True)
    result = models.OneToOneField(Result, on_delete=models.PROTECT)
    public = models.BooleanField(default=False)
    history = HistoricalRecords()

    def get_choro_map(self) -> str or NoReturn:
        result_pk = self.result.pk
        result = Result.objects.get(result_pk)
        return result.choropleth if result.choropleth else None

    def latest_comment(self):
        self.comments


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name="comments")
    body = models.CharField(max_length=25000)
    date_published = models.DateTimeField(auto_now_add=True)
    date_last_edit = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("mtn_web.User", on_delete=models.PROTECT, related_name="comments")
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f'Comment from {self.author.first_name} {self.author.last_name} on {self.date_published} to post "{self.post.title}", made {self.date_published}'


class User(AbstractUser):
    @property
    def latest_post(self) -> Post or None:
        try:
            latest_post = self.posts.order_by("-id")[0]
        except IndexError:
            latest_post = None
        return latest_post

    @property
    def recent_posts(self):
        try:
            recent_posts = self.posts.order_by("-id")[1:5]
        except IndexError:
            recent_posts = None
        return recent_posts

    @property
    def recent_comments(self):
        try:
            recent_comments = self.comments.all()[0:5]
        except IndexError:
            recent_comments = None
        return recent_comments

    @property
    def recent_results(self):
        try:
            recent_results = self.results.all()[1:5]
        except IndexError:
            recent_results = None
        return recent_results


register(User)

# ======================================================================================#
# enum help from
#   https://hackernoon.com/using-enum-as-model-field-choice-in-django-92d8b97aaa63
