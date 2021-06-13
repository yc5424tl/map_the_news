from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from mtn_web.models import Article, Category, Comment, Post, Result, Source, Country, Language

from .models import User
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django import forms

admin.site.register(User, UserAdmin)


# class ReadershipCountriesInline(admin.StackedInline):
#     model = Country
#     extra = 1
#     max_num = 1


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


# class ReadershipInline(admin.TabularInline):
#     model = Source.readership_countries.through


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "publishing_country":
    #         kwargs["queryset"] = Country.objects.order_by('display_name')
    #     elif db_field.name == "readership_countries":
    #         kwargs["queryset"] = Country.objects.order_by('display_name')
    #     elif db_field.name == "languages":
    #         kwargs["queryset"] = Language.objects.order_by('display_name')
    #     elif db_field.name == "categories":
    #         kwargs["queryset"] = Category.objects.order_by('display_name')
    #     return super(SourceAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # def get_field_queryset(self, db, db_field, request, **kwargs):
    #     queryset = super().get_field_queryset(db, db_field, request)
    #     if db_field.name == 'publishing_country' or 'readership_countries' or 'categories' or 'languages':
    #         queryset = queryset.order_by('display_name')
    #     return queryset

    # class SourceAdmin(admin.InlineModelAdmin):
    # ordering = ["name"]

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (('name', 'url', 'verified'), ('publishing_country', 'readership_countries'))
        }),
        ('Languages/Categories', {
            'classes': ('collapse', 'wide'),
            'fields': ('languages', 'categories')
        }),
    )

    list_display = (
        "id",
        "name",
        "publishing_country",
        "url",
        "verified"
    )

    # @admin.display(ordering='publishing_country__display_name')
    # def publishing_country_display_name(self, obj):
    #     return obj.publishing_country.display_name

    # @admin.display(ordering='readership_countries__display_name')
    # def readership_countries_display_name(self, obj):
    #     return obj.readership_countries.display_name

    list_select_related = (
        "publishing_country",
    )

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

    # inlines = [ReadershipInline,]
    # exclude = ('readership_countries', )

    # inlines = (ReadershipCountriesInline,)

    # def get_form(self, request, obj=None, **kwargs):
    #         form = super(SourceAdmin, self).get_form(request, obj, **kwargs)
    #         form.base_fields['publishing_country'].queryset = form.base_fields['publishing_country'].queryset.order_by('display_name')
    #         form.base_fields['readership_countries'].queryset = form.base_fields['readership_countries'].queryset.order_by('display_name')
    #         form.base_fields['categories'].queryset = form.base_fields['categories'].queryset.order_by('display_name')
    #         form.base_fields['languages'].queryset = form.base_fields['languages'].queryset.order_by('display_name')
    #         return form


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "alpha2_code", "display_name", "alphanum_name")
    list_editable = ("alpha2_code", "display_name", "alphanum_name")
    # inlines = [ReadershipInline, ]


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("id", "alpha2_code", "display_name", "alphanum_name")
    list_editable = ("alpha2_code", "display_name", "alphanum_name")
