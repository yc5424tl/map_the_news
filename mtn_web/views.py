import logging

from logging import Logger
from typing import NoReturn
import pycountry
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.template import RequestContext
from mtn_web.constructor import Constructor
from mtn_web.forms import (
    CustomUserCreationForm,
    NewQueryForm,
    NewPostForm,
    EditPostForm,
    EditCommentForm,
    NewCommentForm,
)

from mtn_web.geo_data_mgr import GeoDataManager
from mtn_web.geo_map_mgr import GeoMapManager  # , geo_data_mgr
from mtn_web.models import Result, Source, Post, Comment, Category, QueryTypeChoice
from mtn_web.query_mgr import Query


logging.basicConfig(filename="news_map.log", level=logging.INFO)
logger = Logger(__name__)

constructor = Constructor()
geo_map_mgr = GeoMapManager()


@transaction.atomic
def index(request) -> render:
    if request.method == "GET":
        form = AuthenticationForm()
        return render(request, "general/index.html", {"form": form})
    else:
        return HttpResponseBadRequest('Unsupported Request Method')

def register_user(request: requests.request) -> render or redirect:
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("view_user", user.pk)
        else:
            messages.info(request, message=form.errors)
            form = CustomUserCreationForm()
            return render(
                request=request,
                template_name="general/new_user.html",
                context={"form": form}
            )
    if request.method == "GET":
        form = CustomUserCreationForm()
        return render(request, "general/new_user.html", {"form": form})


def login_user(request: requests.request) -> render or redirect:
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("view_user", user.pk)
        form = AuthenticationForm()
        messages.error(
            request, "Incorrect Password and/or Username", extra_tags="error"
        )
        return render(request, "general/login_user.html", {"form": form})
    if request.method == "GET":
        form = AuthenticationForm()
        return render(request, "general/login_user.html", {"form": form})


def logout_user(request: requests.request) -> NoReturn:
    if request.user.is_authenticated:
        messages.info(request, "Logout Successful", extra_tags="alert")


def get_query_type(qm_focus: str):
    if qm_focus == "QueryTypeChoice.ALL" or "all".casefold():
        query_type = QueryTypeChoice.ALL
    elif qm_focus == "QueryTypeChoice.HDL" or "headlines".casefold():
        query_type = QueryTypeChoice.HDL
    else:
        logger.log(
            level=logging.ERROR,
            msg=f"query_type not found in get_query_type for qm_focus of {qm_focus}",
        )
        query_type = None
    return query_type


@login_required()
def new_query(request: requests.request) -> render or redirect:
    if request.method == "GET":
        form = NewQueryForm()
        return render(request, "general/new_query.html", {"search_form": form})
    elif request.method == "POST":
        gdm = GeoDataManager()
        if gdm.verify_geo_data():
            query_mgr = Query(
                arg=request.POST.get("argument"),
                focus=get_query_type(request.POST.get("query_type")),
            )
            have_endpoint = query_mgr.get_endpoint()
            if have_endpoint is False:
                messages.info(
                    request,
                    message="Unable to contact endpoint to complete your query.",
                )
                return redirect("new_query", messages=messages)
            query_data = query_mgr.execute_query()
            article_data, article_count = query_data[0], query_data[1]
            result = Result.objects.create(
                query_type=query_mgr.focus,
                argument=query_mgr.arg,
                data=article_data,
                author=request.user,
                articles_per_country=gdm.result_dict
            )
            result.save()
            article_list = constructor.build_article_data(article_data, result)
            # TODO get len of list for # of articles, in loop below map each to country
            for article in article_list:
                country_code = geo_map_mgr.map_source(
                    source_country=article.source_country
                )
                gdm.add_result(country_code)
            data_tup = geo_map_mgr.build_choropleth(
                result.argument, result.query_type, gdm
            )
            if data_tup is None:
                return redirect("index", messages="build choropleth returned None")
            else:
                global_map, filename = data_tup[0], data_tup[1]
                result.choro_html = global_map.get_root().render()
                result.filename = filename
                result.choropleth = global_map._repr_html_()
                result.article_count = article_count
                result.article_data_len = len(article_data)
                result.save()
                return redirect("view_result", result.pk)
        else:
            # redirect("handler404", request)
            messages.info(request, message="Mapping Resources Unavailable")
            return redirect("index", messages=messages)
    else:
        # raise Http404("Unsupported Request Method.")
        raise HttpResponseBadRequest

@login_required()
def view_result(request, result_pk: int):
    result = get_object_or_404(Result, pk=result_pk)
    logger.log(level=logging.ERROR, msg=f'result.articles_per_country == {result.articles_per_country}')
    return render(
        request,
        "general/view_result.html",
        {
            "result": result,
            "query_author": result.author,
            "articles": result.articles.all(),
            "choro_map": result.choropleth,
            "choro_html": result.choro_html,
            "filename": result.filename,
            "article_count": result.article_count,
            "article_data_len": result.article_data_len,
            'country_articles': result.articles_per_country,
        },
    )


@login_required()
def view_public_posts(request):
    posts = Post.objects.order_by("-id").all()
    paginator = Paginator(posts, 10)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "general/view_public_posts.html", {"posts": posts})


@login_required()
def delete_comment(request, comment_pk: int):
    if request.method == "POST":
        comment = get_object_or_404(Comment, pk=comment_pk)
        post_pk = comment.post.pk
        if comment.author.pk == request.user.pk:
            comment.delete()
            messages.info(request, message="Comment Deleted")
        else:
            messages.info(request, message="Unauthorized")
        return redirect("view_post", post_pk, messages=messages)


@login_required()
def delete_result(request, result_pk: int):
    Result.objects.filter(pk=result_pk).delete()
    messages.info(request, "Result Successfully Deleted")
    return redirect("new_result")


@login_required()
def view_user(request, member_pk):
    try:
        user = get_user_model().objects.get(pk=member_pk)

        try:
            last_post = user.posts.order_by("-id")[0]
        except IndexError:
            last_post = None

        try:
            recent_posts = user.posts.order_by("-id")[1:5]
        except IndexError:
            recent_posts = None

        try:
            recent_comments = None
            has_comments = user.comments.all()[0]
            if has_comments:
                recent_comments = user.comments.all()[0:5]
        except IndexError:
            recent_comments = None

        try:
            recent_results = None
            has_results = user.results.all()[0]
            if has_results:
                recent_results = user.results.all()[1:5]
        except IndexError:
            recent_results = None

        return render(
            request,
            "general/view_user.html",
            {
                "member": user,
                "posts": recent_posts,
                "comments": recent_comments,
                "last_post": last_post,
                "queries": recent_results,
            },
        )
    except get_user_model().DoesNotExist:
        raise Http404("User Not Found")


@login_required()
def new_post(request):
    if request.method == "GET":
        form = NewPostForm()
        result_pk = form["result_pk"].value()
        result = get_object_or_404(Result, pk=result_pk)
        return render(
            request, "general/new_post.html", {"form": form, "result": result, 'country_articles': result.articles_per_country}
        )
    elif request.method == "POST":
        form = NewPostForm(request.POST)
        if request.user.is_authenticated:
            try:
                pk = request.user.pk
                author = get_user_model().objects.get(pk=pk)
                if form.is_valid():
                    title = form.cleaned_data.get("title")
                    public = request.POST.get("save_radio")
                    body = form.cleaned_data.get("body")
                    result_pk = request.POST.get("result_pk")
                    result = Result.objects.get(pk=result_pk)
                    post = Post(
                        title=title,
                        public=public,
                        body=body,
                        result=result,
                        author=author,
                    )
                    post.save()
                    result.archived = True
                    result.save()
                    return redirect("view_post", post.pk)
                else:
                    logger.log(level=logging.ERROR, msg=form.errors)
                    messages.error = (request, form.errors)
                    return redirect("new_post")
            except get_user_model().DoesNotExist:
                return PermissionDenied



@login_required()
def update_post(request, post_pk):
    return render(request, "general/update_post.html", {"post_pk": post_pk})


@login_required()
def update_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == "GET":
        form = EditCommentForm(instance=comment)
        return render(
            request, "general/update_comment.html", {"form": form, "comment": comment}
        )
    elif request.method == "POST":
        form = EditCommentForm()
        if form.is_valid():
            form.save()
            messages.info(request, "Comment Updated!")
        else:
            messages.error(request, form.errors)
        return redirect("view_comment", comment_pk=comment_pk)


@login_required()
def view_post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        form = EditPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.info(request, "Post Details Updated")
        else:
            messages.error(request, form.errors)
        return redirect("post_details", post_pk=post_pk)
    else:
        post = get_object_or_404(Post, pk=post_pk)
        result = post.result
        articles = post.result.articles.all()
        if post.author.id == request.user.id:
            edit_post_form = EditPostForm(
                instance=Post
            )  # Pre-populate form with the post's current field values
            return render(
                request,
                "general/view_post.html",
                {
                    "post": post,
                    "edit_post_form": edit_post_form,
                    "result": result,
                    "articles": articles,
                    'country_articles': result.articles_per_country
                },
            )
        else:
            return render(
                request,
                "general/view_post.html",
                {
                    "post": post,
                    "result": result,
                    "articles": articles,
                    'country_articles': result.articles_per_country
                },
            )


def view_sources(request):
    source_dict_list = [
        {
            "country": source.country_full_name,
            "name": source.name,
            "language": source.language_full_name,
            "categories": [category.name for category in source.categories.all()],
            "url": source.url,
        }
        for source in Source.objects.all()
    ]
    category_dict_list = [
        {
            "cat": category.name,
            "src_list": [
                {
                    "name": source.name,
                    "country": source.country_full_name,
                    "language": source.language_full_name,
                    "url": source.url,
                }
                for source in category.sources.all()
            ],
        }
        for category in Category.objects.all()
    ]
    return render(
        request,
        "general/view_sources.html",
        {"sources": source_dict_list, "categories": category_dict_list},
    )


def lang_a2_to_name(source):
    try:
        return pycountry.languages.lookup(source.language).name
    except LookupError:
        return source.language


def country_a2_to_name(source):
    try:
        return pycountry.countries.lookup(source.country).name
    except LookupError:
        return source.country


@login_required()
def delete_post(request):
    if request.method != 'POST':
        raise HttpResponseBadRequest
    pk = request.POST["post_pk"]
    post = get_object_or_404(Post, pk=pk)
    if post.author.id == request.user.id:
        post.delete()
        messages.info(request, "Post Removed")
        return redirect("index")
    else:
        messages.error(request, "Action Not Authorized")
        return redirect("view_post", pk=pk)


@login_required()
def new_comment(request, post_pk):
    if request.method == "GET":
        form = NewCommentForm()
        post = Post.objects.get(pk=post_pk)
        return render(request, "general/new_comment.html", {"post": post, "form": form})
    elif request.method == "POST":
        c_post = Post.objects.get(pk=post_pk)
        c_body = request.POST.get("body")
        c_author = get_user_model().objects.get(pk=request.user.pk)
        c = Comment.objects.create(post=c_post, body=c_body, author=c_author)
        c.save()
        return redirect("view_comment", c.pk)


@login_required()
def view_comment(request, comment_pk):
    try:
        comment = Comment.objects.get(pk=comment_pk)
        return render(request, "general/view_comment.html", {"comment": comment})
    except Comment.DoesNotExist:
        raise Http404("Comment Not Found")


@login_required()
def delete_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    last_url = request.POST["redirect_url"]
    messages.info(request, "Failed to Delete Comment")
    return redirect(last_url)


# TODO def password_reset(request)


def view_choro(request: requests.request, result_pk) -> render:
    # result = Result.objects.get(pk=result_pk)
    result = get_object_or_404(Result, pk=result_pk)
    return render(request, "general/view_choro.html", {"result": result})


# BAD REQUEST
def handler400(request, exception):
  #  return render(request=request, template_name='error/400.html', context=locals())
    return render(
        request=request,
        template_name="error/400.html",
        context=locals(),
        status=400
    )


# UNAUTHORIZED
def handler401(request, exception):
    return render(
        request=request,
        template_name="error/401.html",
        context=locals(),
        status=401
    )


# PERMISSION DENIED, called by raising PermissionDenied
def handler403(request, exception):
    # return render(request=request, template_name='error/403.html', context=locals())
    return render(
        request=request,
        template_name='error/403.html',
        context=locals(),
        status=403
    )


# PAGE NOT FOUND
def handler404(request, exception):
    context = RequestContext(request)
    # return render(request=request, template_name="error/404.html", context=locals())
    return render(
        request=request,
        template_name="error/404.html",
        context=locals(),
        status=404
    )


#  SERVER ERROR
def handler500(request):
    # return render(request, "error/500.html", status=500)
    return render(
        request=request,
        template_name="error/500.html",
        status=500
    )


def report_error(request):
    return render(
        request=request,
        template_name="error/report.html",
        context=locals(),
        status=200
    )
