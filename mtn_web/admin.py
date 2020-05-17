from django.contrib import admin

from mtn_web.models import Source, Post, Result, Article, Comment, Category

from django.contrib.auth.admin import UserAdmin
from .models import User


admin.site.register(User, UserAdmin)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "date_published", "source", "result")


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "argument",
        "query_type",
        "filename",
        "filepath",
        "author",
        "archived",
        "date_created",
        "public",
        "choropleth",
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "date_published",
        "author",
        "result",
        "public",
        "date_last_edit",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("body", "date_published", "date_last_edit", "author", "post")


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "language", "url")
    list_editable = ("country", "language", "url")
    list_filter = ("country", "language")
    list_display_links = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
