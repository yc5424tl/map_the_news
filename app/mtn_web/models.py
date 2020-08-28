from enum import Enum
from typing import NoReturn
import pycountry
from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.postgres.fields import JSONField
from django.db.models import JSONField


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
    public = models.BooleanField(default=False)
    query_type = models.CharField(
        max_length=50,
        choices=[(tag, tag.value) for tag in QueryTypeChoice],
        default=QueryTypeChoice.ALL,
    )
    author = models.ForeignKey(
        "mtn_web.User", on_delete=models.PROTECT, related_name="results"
    )
    archived = models.BooleanField(default=False)
    article_count = models.IntegerField(default=0)
    article_data_len = models.IntegerField(default=0)
    articles_per_country = JSONField(max_length=20000, null=True, blank=True)

    def __str__(self):
        details = (
            f"Argument: {self.argument}\n Query Type: {self.query_type}\n Author: {self.author}\n Archived: {self.archived}\n"
            f"Public: {self.public}\n Data[:500]: {self.data[:500]}\n ChoroHTML: {self.choro_html[:500]}"
        )
        if self.filename:
            details = f"{details}\nFilename = {self.filename}"
        return details

    @property
    def date_created_readable(self) -> str:
        return f"{self.date_created.month}, {self.date_created.day}, {self.date_created.year}"


class Category(models.Model):

    name = models.CharField(max_length=50, unique=True)


class Source(models.Model):
    name = models.CharField(max_length=500)
    country = models.CharField(max_length=3)
    language = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category, related_name="sources")
    url = models.URLField(blank=True, default="", max_length=150)
    verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def country_display_name(self) -> str:
        try:
            full_name = pycountry.countries.lookup(self.country).name
            comma_index = full_name.find(',')
            if comma_index == -1:  # no comma in string
                return full_name
            else:
                '''
                substring up to first comma, i.e. "Bolivia, Plurinational State of" will return "Bolivia".
                This is done as the country names are used to:
                    - generate element id's in templates, and neither spaces or commas are allowed.
                    - As a user-friendly alternative to presenting iso-alpha2/3 codes in templates.
                '''
                substring = full_name[:comma_index]
                return substring
        except LookupError:
            return self.country

    @property
    def country_alphanum_name(self) -> str:
        try:
            full_name = pycountry.countries.lookup(self.country).name
            if full_name.contains(' '):
                filter_alphanum = filter(str.isalnum, full_name)
                alphanum_string = "".join(filter_alphanum)
                return alphanum_string
            return full_name
        except LookupError:
            return self.country

    @property
    def language_readable_full_name(self) -> str:
        try:
            display_name = pycountry.languages.get(alpha_2=self.language).name
            return display_name
        except LookupError:
            return self.language

    @property
    def language_alphanum_full_name(self) -> str:
        try:
            full_name = pycountry.languages.get(alpha_2=self.language).name
            alphanum_filter = filter(str.isalnum, full_name)
            alphanum_string = "".join(alphanum_filter)
            return alphanum_string
        except LookupError:
            return self.language


class Article(models.Model):
    article_url = models.URLField(max_length=1000)
    author = models.CharField(max_length=150)
    date_published = models.DateTimeField(default=None, null=True, blank=True)
    description = models.CharField(max_length=2500)
    image_url = models.URLField(max_length=1000, default=None, blank=True, null=True)
    result = models.ForeignKey(
        Result,
        on_delete=models.CASCADE,
        related_name="articles",
        related_query_name="article",
    )
    source = models.ForeignKey(
        Source,
        on_delete=models.PROTECT,
        related_name="articles",
        related_query_name="article",
    )
    title = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.title}, {self.author}, {self.date_published}, {self.source.name}"

    @property
    def source_country(self) -> str:
        return self.source.country


class Post(models.Model):
    title = models.CharField(max_length=300, default="", null=True, blank=True)
    body = models.CharField(max_length=50000, default="", null=True, blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        "mtn_web.User", on_delete=models.PROTECT, related_name="posts"
    )
    date_last_edit = models.DateTimeField(auto_now_add=True)
    result = models.OneToOneField(Result, on_delete=models.PROTECT)
    public = models.BooleanField(default=False)

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
    author = models.ForeignKey(
        "mtn_web.User", on_delete=models.PROTECT, related_name="comments"
    )

    def __str__(self) -> str:
        return f'Comment from {self.author.first_name} {self.author.last_name} on {self.date_published} to post "{self.post.title}", made {self.date_published}'


class User(AbstractUser):
    pass


# ======================================================================================#
# enum help from
#   https://hackernoon.com/using-enum-as-model-field-choice-in-django-92d8b97aaa63
