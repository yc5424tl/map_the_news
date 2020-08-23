from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from mtn_web.models import Article, Category, Comment, Post, Result, Source

from .models import User

admin.site.register(User, UserAdmin)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "date_published", "source", "result", "image_url", "article_url")
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
        # "choropleth"
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
    list_display = ("id", "name", "country", "language", "url", "verified")
    list_editable = ("country", "language", "url", "verified")
    list_filter = ("country", "language", "verified")
    list_display_links = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
