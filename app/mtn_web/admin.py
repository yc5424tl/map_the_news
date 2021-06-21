from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin

from mtn_web.models import Article, Category, Comment, Country, Language, Post, Result, Source, User

admin.site.register(User, UserAdmin)


@admin.register(Article)
class ArticleAdmin(SimpleHistoryAdmin):
    list_display = ("id", "title", "author", "date_published", "source", "result", "image_url", "article_url")
    list_editable = ("image_url", "article_url")
    list_filter = ("author", "source", "date_published", "result")
    list_display_links = ("author", "source", "result")


@admin.register(Result)
class ResultAdmin(SimpleHistoryAdmin):
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
class PostAdmin(SimpleHistoryAdmin):
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
class CommentAdmin(SimpleHistoryAdmin):
    list_display = ("id", "body", "date_published", "date_last_edit", "author", "post")
    list_filter = ("author", "date_published", "date_last_edit")
    list_display_links = ("author", "post")
    list_editable = ("body",)


@admin.register(Source)
class SourceAdmin(SimpleHistoryAdmin):

    fieldsets = (
        (None, {"classes": ("wide",), "fields": (("name", "url", "verified"), ("publishing_country", "readership_countries"))}),
        ("Languages/Categories", {"classes": ("collapse", "wide"), "fields": ("languages", "categories")}),
    )

    list_display = ("id", "name", "publishing_country", "url", "verified")

    list_select_related = ("publishing_country",)

    list_editable = (
        "url",
        "verified",
        "publishing_country",
    )

    list_filter = ("verified", "publishing_country")

    list_display_links = ["id", "name"]

    filter_horizontal = (
        "readership_countries",
        "languages",
    )

    actions =["update_readerships"]

    @admin.action(description='Update Readership Countries and Country of Publication')
    def update_readerships(self, request, queryset):
        if 'exec' in request.POST:
            publishing_country = Country.objects.get(pk=request.POST['publishing_country'])
            queryset.update(publishing_country=publishing_country)
            readership_country = Country.objects.get(pk=request.POST['readership_country'])
            for source in queryset:
                if readership_country not in source.readership_countries:
                    source.readership_countries.add(readership_country)
            self.message_user(request, f'Updated publishing/readership data on {queryset.count()} source(s)')
            return HttpResponseRedirect(request.get_full_path())
        countries = Country.objects.all()
        return render(request, 'admin/readership_update_intermediate.html', context={"sources": queryset, "countries": countries})


@admin.register(Category)
class CategoryAdmin(SimpleHistoryAdmin):
    list_display = ("id", "name")


@admin.register(Country)
class CountryAdmin(SimpleHistoryAdmin):
    list_display = ("id", "alpha2_code", "display_name", "alphanum_name")
    list_editable = ("alpha2_code", "display_name", "alphanum_name")


@admin.register(Language)
class LanguageAdmin(SimpleHistoryAdmin):
    list_display = ("id", "alpha2_code", "display_name", "alphanum_name")
    list_editable = ("alpha2_code", "display_name", "alphanum_name")
