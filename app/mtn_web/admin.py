from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from mtn_web.models import Article, Category, Comment, Post, Result, Source, Country, Language

from .models import User
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django import forms

admin.site.register(User, UserAdmin)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "date_published",
        "source",
        "result",
        "image_url",
        "article_url"
    )
    list_editable = ("image_url", "article_url")
    list_filter = ("author", "source", "date_published", "result")
    list_display_links = ("author", "source", "result")


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "argument",
        "query_type",
        "author",
        "archived",
        "public",
        "filename",
        "filepath",
        "date_created",
    )
    list_editable = ("query_type", "archived", "public", "filename", "filepath")
    list_filter = ("query_type", "archived", "public", "author", "argument")
    list_display_links = ("author",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "date_published",
        "author",
        "result",
        "public",
        "date_last_edit",
    )
    list_filter = ("author", "public", "date_published", "date_last_edit")
    list_editable = ("public", "title")
    list_display_links = ("author", "result")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "body", "date_published", "date_last_edit", "author", "post")
    list_filter = ("author", "date_published", "date_last_edit")
    list_display_links = ("author", "post")
    list_editable = ("body",)


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "country",
        "language",
        "country_alpha2_code",
        "country_display_name",
        "country_alphanum_name",
        "language_alpha2_code",
        "language_display_name",
        "language_alphanum_name",
        "publishing_country",
        "url",
        "verified"
    )
    list_editable = (
        "country",
        "language",
        "url",
        "verified",
        "country_alpha2_code",
        "country_display_name",
        "country_alphanum_name",
        "language_alpha2_code",
        "language_display_name",
        "language_alphanum_name",
        "publishing_country",
    )
    list_filter = ("country", "language", "verified", )
    list_display_links = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "alpha2_code", "display_name", "alphanum_name")
    list_editable = ("alpha2_code", "display_name", "alphanum_name")


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("id", "alpha2_code", "display_name", "alphanum_name")
    list_editable = ("alpha2_code", "display_name", "alphanum_name")
