import logging
from typing import NoReturn

import pycountry
import requests
from mtn_web.constructor import Constructor
from mtn_web.country_data import iso_codes
from mtn_web.decorators import query_inspection
from mtn_web.forms import CustomUserCreationForm, EditCommentForm, EditPostForm, NewCommentForm, NewPostForm, NewQueryForm, UserLoginForm
from mtn_web.geo_data_mgr import GeoDataManager
from mtn_web.geo_map_mgr import GeoMapManager
from mtn_web.models import Article, Category, Comment, Country, Language, Post, QueryTypeChoice, Result, Source
from mtn_web.query_mgr import Query
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import transaction
from django.db.models import Prefetch
from django.http import HttpResponseBadRequest
from django.shortcuts import Http404, get_object_or_404, redirect, render
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DeleteView, DetailView, ListView, TemplateView

log = logging.getLogger(__name__)


constructor = Constructor()
geo_map_mgr = GeoMapManager()


# ====================================== #
#                                        #
#  ██╗███╗```██╗██████╗`███████╗██╗``██╗ #
#  ██║████╗``██║██╔══██╗██╔════╝╚██╗██╔╝ #
#  ██║██╔██╗`██║██║``██║█████╗```╚███╔╝` #
#  ██║██║╚██╗██║██║``██║██╔══╝```██╔██╗` #
#  ██║██║`╚████║██████╔╝███████╗██╔╝`██╗ #
#  ╚═╝╚═╝``╚═══╝╚═════╝`╚══════╝╚═╝``╚═╝ #
#  ````````````````````````````````````` #
# ====================================== #


@transaction.atomic
def index(request: requests.request) -> render:
    if request.method == "GET":
        form = AuthenticationForm()
        return render(request, "general/index.html", {"form": form})
    else:
        return HttpResponseBadRequest("Unsupported Request Method")


# ==================================================================================================== #
#                                                                                                      #
#  ██████╗`███████╗`██████╗`██╗███████╗████████╗███████╗██████╗`````██╗```██╗███████╗███████╗██████╗`  #
#  ██╔══██╗██╔════╝██╔════╝`██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗````██║```██║██╔════╝██╔════╝██╔══██╗  #
#  ██████╔╝█████╗``██║``███╗██║███████╗```██║```█████╗``██████╔╝````██║```██║███████╗█████╗``██████╔╝  #
#  ██╔══██╗██╔══╝``██║```██║██║╚════██║```██║```██╔══╝``██╔══██╗````██║```██║╚════██║██╔══╝``██╔══██╗  #
#  ██║``██║███████╗╚██████╔╝██║███████║```██║```███████╗██║``██║````╚██████╔╝███████║███████╗██║``██║  #
#  ╚═╝``╚═╝╚══════╝`╚═════╝`╚═╝╚══════╝```╚═╝```╚══════╝╚═╝``╚═╝`````╚═════╝`╚══════╝╚══════╝╚═╝``╚═╝  #
#  ``````````````````````````````````````````````````````````````````````````````````````````````````  #
# ==================================================================================================== #


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
            return render(request=request, template_name="general/new_user.html", context={"form": form})

    if request.method == "GET":
        return render(request, "general/new_user.html", {"form": CustomUserCreationForm})

    else:  # request.method != 'GET' or 'POST'
        return HttpResponseBadRequest("Unsupported Request Method")


# ============================================================================== #
#                                                                                #
#  ██╗      ██████╗  ██████╗ ██╗███╗   ██╗    ██╗   ██╗███████╗███████╗██████╗   #
#  ██║     ██╔═══██╗██╔════╝ ██║████╗  ██║    ██║   ██║██╔════╝██╔════╝██╔══██╗  #
#  ██║     ██║   ██║██║  ███╗██║██╔██╗ ██║    ██║   ██║███████╗█████╗  ██████╔╝  #
#  ██║     ██║   ██║██║   ██║██║██║╚██╗██║    ██║   ██║╚════██║██╔══╝  ██╔══██╗  #
#  ███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║    ╚██████╔╝███████║███████╗██║  ██║  #
#  ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝     ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝  #
# ============================================================================== #


def login_user(request: requests.request) -> render or redirect:
    if request.method == "POST":
        #form = AuthenticationForm(request.POST)
        form = UserLoginForm(request.POST)
        if form.is_valid():
            #username = request.POST['username']
            #password = request.POST['password']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("view_user", user.pk)
        else:
            messages.error(request, "Incorrect Password and/or Username", extra_tags="error")
            return render(request, "registration/login_user.html", {"form": UserLoginForm})
            #return render(request, "registration/login_user.html", {"form": AuthenticationForm})

    elif request.method == "GET":
        #form = AuthenticationForm()
        form = UserLoginForm()
        return render(request, "registration/login_user.html", {"form": form})

    else:  # request.method != 'GET or 'POST'
        return HttpResponseBadRequest("Unsupported Request Method")


# ============================================================================================ #
#                                                                                              #
#  ██╗      ██████╗  ██████╗  ██████╗ ██╗   ██╗████████╗    ██╗   ██╗███████╗███████╗██████╗   #
#  ██║     ██╔═══██╗██╔════╝ ██╔═══██╗██║   ██║╚══██╔══╝    ██║   ██║██╔════╝██╔════╝██╔══██╗  #
#  ██║     ██║   ██║██║  ███╗██║   ██║██║   ██║   ██║       ██║   ██║███████╗█████╗  ██████╔╝  #
#  ██║     ██║   ██║██║   ██║██║   ██║██║   ██║   ██║       ██║   ██║╚════██║██╔══╝  ██╔══██╗  #
#  ███████╗╚██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝   ██║       ╚██████╔╝███████║███████╗██║  ██║  #
#  ╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝    ╚═╝        ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝  #
# ============================================================================================ #


def logout_user(request: requests.request) -> NoReturn:
    if request.user.is_authenticated:
        messages.info(request, "Logout Successful", extra_tags="alert")


# ============================================================================ #
#                                                                              #
#  ███╗   ██╗███████╗██╗    ██╗     ██████╗ ██╗   ██╗███████╗██████╗ ██╗   ██╗ #
#  ████╗  ██║██╔════╝██║    ██║    ██╔═══██╗██║   ██║██╔════╝██╔══██╗╚██╗ ██╔╝ #
#  ██╔██╗ ██║█████╗  ██║ █╗ ██║    ██║   ██║██║   ██║█████╗  ██████╔╝ ╚████╔╝  #
#  ██║╚██╗██║██╔══╝  ██║███╗██║    ██║▄▄ ██║██║   ██║██╔══╝  ██╔══██╗  ╚██╔╝   #
#  ██║ ╚████║███████╗╚███╔███╔╝    ╚██████╔╝╚██████╔╝███████╗██║  ██║   ██║    #
#  ╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝      ╚══▀▀═╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝    #
# ============================================================================ #


@login_required()
def new_query(request: requests.request) -> render or redirect or HttpResponseBadRequest:

    if request.method == "GET":
        form = NewQueryForm()
        return render(request, "general/new_query.html", {"search_form": form})

    elif request.method == "POST":
        gdm = GeoDataManager()

        if gdm.verify_geo_data():

            query_mgr = Query(arg=request.POST.get("argument"), focus=get_query_type(request.POST.get("query_type")),)

            have_endpoint = query_mgr.get_endpoint()

            if have_endpoint is False:
                messages.info(
                    request, message="Resource Unavailable",
                )
                return redirect("new_query", messages=messages)

            query_data = query_mgr.execute_query()
            article_data, article_count = query_data[0], query_data[1]

            result = Result.objects.create(
                query_type=query_mgr.focus, argument=query_mgr.arg, data=article_data, author=request.user, articles_per_country=gdm.result_dict,
            )
            result.save()

            article_list = constructor.build_article_data(article_data, result)

            country_src_dict = {}

            for article in article_list:
                source = get_object_or_404(Source, name=article.source)
                try:
                    country_codes = [source.publishing_country.alpha2_code]
                    if source.publishing_country.alpha2_code not in country_src_dict:
                        country_src_dict[source.publishing_country.alpha2_code] = [(source, article),]
                except Exception as exc:
                    log.error(msg=f'Error retrieving publishing country alpha2 code: {exc}')
                if source.readership_countries:
                    for country in source.readership_countries.all():
                        if country != source.publishing_country:
                            try:
                                country_codes.append(country.alpha2_code)
                                if country.alpha2_code not in country_src_dict:
                                    country_src_dict[country.alpha2_code] = [(source, article),]
                                else:
                                    country_src_dict[country.alpha2_code].append((source, article))
                            except Exception as exc:
                                log.error(msg=exc)
                for alpha2_code in country_codes:
                    try:
                        alpha3_code = geo_map_mgr.map_source(source_country=alpha2_code)
                        gdm.add_result(alpha3_code)
                    except Exception as exc:
                        log.error(msg=exc)

            for alpha2_code in country_src_dict:
                print(f'Country: {alpha2_code}\n Sources: {len(country_src_dict[alpha2_code])}\n')

            data_tup = geo_map_mgr.build_choropleth(result.argument, result.query_type, gdm)

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

        else:  # if not gdm.verify_geo_data()
            messages.info(request, message="Mapping Resources Unavailable")
            return redirect("index", messages=messages)

    else:  # if request.method != (POST or GET)
        return HttpResponseBadRequest("Unsupported Request Method")


# ================================================================================== #
#                                                                                    #
#  ██╗   ██╗██╗███████╗██╗    ██╗    ██████╗ ███████╗███████╗██╗   ██╗██╗  ████████╗ #
#  ██║   ██║██║██╔════╝██║    ██║    ██╔══██╗██╔════╝██╔════╝██║   ██║██║  ╚══██╔══╝ #
#  ██║   ██║██║█████╗  ██║ █╗ ██║    ██████╔╝█████╗  ███████╗██║   ██║██║     ██║    #
#  ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║    ██╔══██╗██╔══╝  ╚════██║██║   ██║██║     ██║    #
#   ╚████╔╝ ██║███████╗╚███╔███╔╝    ██║  ██║███████╗███████║╚██████╔╝███████╗██║    #
#    ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝    #
# ================================================================================== #


@login_required()
def view_result(request: requests.request, result_pk: int) -> render:  # replacing country alpha-2 iso codes with full names for viewing in template
    result = get_object_or_404(Result, pk=result_pk)
    serbian_article_count = result.articles_per_country.pop('CS-KM', False) # returns False if key not present
    country_articles = {pycountry.countries.get(alpha_3=a3_code).name:result.articles_per_country[a3_code] for a3_code in result.articles_per_country}
    if serbian_article_count:
        country_articles['Serbia'] = serbian_article_count
    return render(request, "general/view_result.html", {"result": result, "country_articles": country_articles})


# ============================================================================================================================== #
#                                                                                                                                #
#  ██╗```██╗██╗███████╗██╗````██╗````██████╗`██╗```██╗██████╗`██╗`````██╗`██████╗````██████╗``██████╗`███████╗████████╗███████╗  #
#  ██║```██║██║██╔════╝██║````██║````██╔══██╗██║```██║██╔══██╗██║`````██║██╔════╝````██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝██╔════╝  #
#  ██║```██║██║█████╗``██║`█╗`██║````██████╔╝██║```██║██████╔╝██║`````██║██║`````````██████╔╝██║```██║███████╗```██║```███████╗  #
#  ╚██╗`██╔╝██║██╔══╝``██║███╗██║````██╔═══╝`██║```██║██╔══██╗██║`````██║██║`````````██╔═══╝`██║```██║╚════██║```██║```╚════██║  #
#  `╚████╔╝`██║███████╗╚███╔███╔╝````██║`````╚██████╔╝██████╔╝███████╗██║╚██████╗````██║`````╚██████╔╝███████║```██║```███████║  #
#  ``╚═══╝``╚═╝╚══════╝`╚══╝╚══╝`````╚═╝``````╚═════╝`╚═════╝`╚══════╝╚═╝`╚═════╝````╚═╝``````╚═════╝`╚══════╝```╚═╝```╚══════╝  #
#  ````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````  #
# ============================================================================================================================== #


@login_required()
def view_public_posts(request: requests.request) -> render:
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


# ========================================================================================================================= #
#                                                                                                                           #
#  ██████╗`███████╗██╗`````███████╗████████╗███████╗`````██████╗`██████╗`███╗```███╗███╗```███╗███████╗███╗```██╗████████╗  #
#  ██╔══██╗██╔════╝██║`````██╔════╝╚══██╔══╝██╔════╝````██╔════╝██╔═══██╗████╗`████║████╗`████║██╔════╝████╗``██║╚══██╔══╝  #
#  ██║``██║█████╗``██║`````█████╗`````██║```█████╗``````██║`````██║```██║██╔████╔██║██╔████╔██║█████╗``██╔██╗`██║```██║```  #
#  ██║``██║██╔══╝``██║`````██╔══╝`````██║```██╔══╝``````██║`````██║```██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝``██║╚██╗██║```██║```  #
#  ██████╔╝███████╗███████╗███████╗```██║```███████╗````╚██████╗╚██████╔╝██║`╚═╝`██║██║`╚═╝`██║███████╗██║`╚████║```██║```  #
#  ╚═════╝`╚══════╝╚══════╝╚══════╝```╚═╝```╚══════╝`````╚═════╝`╚═════╝`╚═╝`````╚═╝╚═╝`````╚═╝╚══════╝╚═╝``╚═══╝```╚═╝```  #
#  ```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````  #
# ========================================================================================================================= #


@login_required()
def delete_comment(request: requests.request, comment_pk: int) -> HttpResponseBadRequest or redirect:
    if request.method != "POST":
        return HttpResponseBadRequest("Unsupported Request Method")
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.author.pk == request.user.pk:
        comment.delete()
        messages.info(request, message="Comment Deleted")
    else:
        messages.info(request, message="Unauthorized")
    return redirect("view_post", comment.post_pk, messages=messages)


# ===================================================================================================== #
#                                                                                                       #
#  ██████╗`███████╗██╗`````███████╗████████╗███████╗````██████╗`███████╗███████╗██╗```██╗██╗``████████╗ #
#  ██╔══██╗██╔════╝██║`````██╔════╝╚══██╔══╝██╔════╝````██╔══██╗██╔════╝██╔════╝██║```██║██║``╚══██╔══╝ #
#  ██║``██║█████╗``██║`````█████╗`````██║```█████╗``````██████╔╝█████╗``███████╗██║```██║██║`````██║``` #
#  ██║``██║██╔══╝``██║`````██╔══╝`````██║```██╔══╝``````██╔══██╗██╔══╝``╚════██║██║```██║██║`````██║``` #
#  ██████╔╝███████╗███████╗███████╗```██║```███████╗````██║``██║███████╗███████║╚██████╔╝███████╗██║``` #
#  ╚═════╝`╚══════╝╚══════╝╚══════╝```╚═╝```╚══════╝````╚═╝``╚═╝╚══════╝╚══════╝`╚═════╝`╚══════╝╚═╝``` #
#  ```````````````````````````````````````````````````````````````````````````````````````````````````` #
# ===================================================================================================== #


@login_required()
def delete_result(request, result_pk: int):
    result = get_object_or_404(Result, pk=result_pk)
    result.delete()
    messages.info(request, message="Result Successfully Deleted")
    return redirect("new_query", messages=messages)


# ===================================================================== #
#                                                                       #
#  ██╗```██╗██╗███████╗██╗````██╗````██╗```██╗███████╗███████╗██████╗`  #
#  ██║```██║██║██╔════╝██║````██║````██║```██║██╔════╝██╔════╝██╔══██╗  #
#  ██║```██║██║█████╗``██║`█╗`██║````██║```██║███████╗█████╗``██████╔╝  #
#  ╚██╗`██╔╝██║██╔══╝``██║███╗██║````██║```██║╚════██║██╔══╝``██╔══██╗  #
#  `╚████╔╝`██║███████╗╚███╔███╔╝````╚██████╔╝███████║███████╗██║``██║  #
#  ``╚═══╝``╚═╝╚══════╝`╚══╝╚══╝``````╚═════╝`╚══════╝╚══════╝╚═╝``╚═╝  #
#  ```````````````````````````````````````````````````````````````````  #
# ===================================================================== #


@login_required()
def view_user(request, member_pk):
    try:
        user = get_user_model().objects.get(pk=member_pk)
        return render(request, "general/view_user.html", {"user": user})
    except get_user_model().DoesNotExist:
        raise Http404("User Not Found")


# ==================================================================== #
#                                                                      #
#  ███╗```██╗███████╗██╗````██╗````██████╗``██████╗`███████╗████████╗  #
#  ████╗``██║██╔════╝██║````██║````██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝  #
#  ██╔██╗`██║█████╗``██║`█╗`██║````██████╔╝██║```██║███████╗```██║```  #
#  ██║╚██╗██║██╔══╝``██║███╗██║````██╔═══╝`██║```██║╚════██║```██║```  #
#  ██║`╚████║███████╗╚███╔███╔╝````██║`````╚██████╔╝███████║```██║```  #
#  ╚═╝``╚═══╝╚══════╝`╚══╝╚══╝`````╚═╝``````╚═════╝`╚══════╝```╚═╝```  #
#  ``````````````````````````````````````````````````````````````````  #
# ==================================================================== #


@login_required()
def new_post(request):

    if request.method == "GET":
        form = NewPostForm()
        result_pk = form["result_pk"].value()
        result = get_object_or_404(Result, pk=result_pk)
        return render(request, "general/new_post.html", {"form": form, "result": result, "country_articles": result.articles_per_country},)

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

                    post = Post(title=title, public=public, body=body, result=result, author=author,)

                    post.save()
                    result.archived = True
                    result.save()
                    return redirect("view_post", post.pk)

                else:  # not form.is_valid
                    log.error(form.errors)
                    messages.error = (request, form.errors)
                    return redirect("new_post")

            except get_user_model().DoesNotExist:
                raise PermissionDenied

        else:  # if not user.is_authenticated
            return redirect("login_user")

    else:  # if request.method != (POST or GET)
        return HttpResponseBadRequest("Unsupported Request Method")


# ========================================================================================= #
#                                                                                           #
#  ██╗```██╗██████╗`██████╗``█████╗`████████╗███████╗````██████╗``██████╗`███████╗████████╗ #
#  ██║```██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝````██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝ #
#  ██║```██║██████╔╝██║``██║███████║```██║```█████╗``````██████╔╝██║```██║███████╗```██║``` #
#  ██║```██║██╔═══╝`██║``██║██╔══██║```██║```██╔══╝``````██╔═══╝`██║```██║╚════██║```██║``` #
#  ╚██████╔╝██║`````██████╔╝██║``██║```██║```███████╗````██║`````╚██████╔╝███████║```██║``` #
#  `╚═════╝`╚═╝`````╚═════╝`╚═╝``╚═╝```╚═╝```╚══════╝````╚═╝``````╚═════╝`╚══════╝```╚═╝``` #
#  ```````````````````````````````````````````````````````````````````````````````````````` #
# ========================================================================================= #


@login_required()
def update_post(request, post_pk):
    return render(request, "general/update_post.html", {"post_pk": post_pk})


# ========================================================================================================================== #
#                                                                                                                            #
#  ██╗```██╗██████╗`██████╗``█████╗`████████╗███████╗`````██████╗`██████╗`███╗```███╗███╗```███╗███████╗███╗```██╗████████╗  #
#  ██║```██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝````██╔════╝██╔═══██╗████╗`████║████╗`████║██╔════╝████╗``██║╚══██╔══╝  #
#  ██║```██║██████╔╝██║``██║███████║```██║```█████╗``````██║`````██║```██║██╔████╔██║██╔████╔██║█████╗``██╔██╗`██║```██║```  #
#  ██║```██║██╔═══╝`██║``██║██╔══██║```██║```██╔══╝``````██║`````██║```██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝``██║╚██╗██║```██║```  #
#  ╚██████╔╝██║`````██████╔╝██║``██║```██║```███████╗````╚██████╗╚██████╔╝██║`╚═╝`██║██║`╚═╝`██║███████╗██║`╚████║```██║```  #
#  `╚═════╝`╚═╝`````╚═════╝`╚═╝``╚═╝```╚═╝```╚══════╝`````╚═════╝`╚═════╝`╚═╝`````╚═╝╚═╝`````╚═╝╚══════╝╚═╝``╚═══╝```╚═╝```  #
#  ````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````  #
# ========================================================================================================================== #


@login_required()
def update_comment(request, comment_pk):

    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == "GET":
        form = EditCommentForm(instance=comment)
        return render(request, "general/update_comment.html", {"form": form, "comment": comment})

    elif request.method == "POST":
        form = EditCommentForm()
        if form.is_valid():
            form.save()
            messages.info(request, "Comment Updated!")
        else:
            messages.error(request, form.errors)
        return redirect("view_comment", comment_pk=comment_pk)

    else:  # request.method != ('GET' or 'POST')
        return HttpResponseBadRequest("Unsupported Request Method")


# ====================================================================== #
#                                                                        #
#  ██╗```██╗██╗███████╗██╗````██╗````██████╗``██████╗`███████╗████████╗  #
#  ██║```██║██║██╔════╝██║````██║````██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝  #
#  ██║```██║██║█████╗``██║`█╗`██║````██████╔╝██║```██║███████╗```██║```  #
#  ╚██╗`██╔╝██║██╔══╝``██║███╗██║````██╔═══╝`██║```██║╚════██║```██║```  #
#  `╚████╔╝`██║███████╗╚███╔███╔╝````██║`````╚██████╔╝███████║```██║```  #
#  ``╚═══╝``╚═╝╚══════╝`╚══╝╚══╝`````╚═╝``````╚═════╝`╚══════╝```╚═╝```  #
#  ````````````````````````````````````````````````````````````````````  #
# ====================================================================== #


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
        if post.author.id == request.user.id:
            edit_post_form = EditPostForm(instance=Post)  # Pre-populate form with the post's current field values
            return render( request,"general/view_post.html", {"post": post, "edit_post_form": edit_post_form})
        else:
            return render(request, "general/view_post.html", {"post": post})


# ============================================================================================== #
#                                                                                                #
#  ██╗```██╗██╗███████╗██╗````██╗````███████╗`██████╗`██╗```██╗██████╗``██████╗███████╗███████╗  #
#  ██║```██║██║██╔════╝██║````██║````██╔════╝██╔═══██╗██║```██║██╔══██╗██╔════╝██╔════╝██╔════╝  #
#  ██║```██║██║█████╗``██║`█╗`██║````███████╗██║```██║██║```██║██████╔╝██║`````█████╗``███████╗  #
#  ╚██╗`██╔╝██║██╔══╝``██║███╗██║````╚════██║██║```██║██║```██║██╔══██╗██║`````██╔══╝``╚════██║  #
#  `╚████╔╝`██║███████╗╚███╔███╔╝````███████║╚██████╔╝╚██████╔╝██║``██║╚██████╗███████╗███████║  #
#  ``╚═══╝``╚═╝╚══════╝`╚══╝╚══╝`````╚══════╝`╚═════╝``╚═════╝`╚═╝``╚═╝`╚═════╝╚══════╝╚══════╝  #
#  ````````````````````````````````````````````````````````````````````````````````````````````  #
# ============================================================================================== #

# TODO turn view_source_groups in to an a template to extend for the views below it
# @cache_page(60 * 60 * 23 + 3599)
def view_source_groups(request):
    if request.method == "GET":
        categories = Category.objects.all().order_by("name").iterator()
        countries = Country.objects.all().order_by("display_name").iterator()
        languages = Language.objects.all().order_by("display_name").iterator()
        return render(request, "general/view_source_groups.html", {"categories": categories, "countries": countries, "languages": languages},)
    else:
        return HttpResponseBadRequest("Unsupported Request Method")


def view_source_detail(request, name):
    source_object = get_object_or_404(Source, name=name)
    target_id = source_object.id
    source_queryset = (
        Source.objects.filter(id=target_id)
        .prefetch_related(
            Prefetch("categories", queryset=Category.objects.only("name").order_by("name")),
            Prefetch("languages", queryset=Language.objects.only("display_name").order_by("display_name")),
            Prefetch("readership_countries", queryset=Country.objects.only("display_name").order_by("display_name")),
        )
        .select_related("publishing_country")
        .only("categories", "languages", "name", "publishing_country", "readership_countries")
    )

    source = [
        {
            "name": source.name,
            "categories": [category.name for category in source.categories.all()],
            "languages": [language.display_name for language in source.languages.all()],
            "publishing_country": source.publishing_country.display_name,
            "readership_countries": [readership.display_name for readership in source.readership_countries.all()],
        }
        for source in source_queryset
    ]

    return render(request, "general/view_source_detail.html", {"source": source})


def view_category_sources(request, name):

    category = get_object_or_404(Category, name=name)

    sources_queryset = (
        category.sources.order_by("name")
        .prefetch_related(
            Prefetch("languages", queryset=Language.objects.only("display_name", "alphanum_name").order_by("display_name")),
            Prefetch("categories", queryset=Category.objects.only("name").order_by("name")),
            Prefetch("readership_countries", queryset=Country.objects.only("display_name", "alphanum_name").order_by("display_name"),),
        )
        .select_related("publishing_country")
        .only("name", "categories", "languages", "publishing_country", "readership_countries")
    )

    sources = [
        {
            "name": source.name,
            "categories": [category.name for category in source.categories.all()],
            "languages": [language.display_name for language in source.languages.all()],
            "publishing_country": source.publishing_country.display_name,
            "readership_countries": [readership.display_name for readership in source.readership_countries.all()],
            "url": source.get_absolute_url(),
        }
        for source in sources_queryset
    ]

    return render(request, "general/view_category_detail.html", {"category": category, "sources": sources})


def view_country_sources(request, alphanum_name):

    country = get_object_or_404(Country, alphanum_name=alphanum_name)

    readership_sources_queryset = (
        country.readership_sources.order_by("name")
        .prefetch_related(
            Prefetch("categories", queryset=Category.objects.only("name").order_by("name")),
            Prefetch("languages", queryset=Language.objects.only("display_name", "alphanum_name").order_by("display_name")),
            Prefetch("readership_countries", queryset=Country.objects.only("display_name", "alphanum_name").order_by("display_name"),),
        )
        .select_related("publishing_country")
        .only("name", "categories", "languages", "publishing_country", "readership_countries")
    )

    readership_sources = [
        {
            "name": source.name,
            "categories": [category.name for category in source.categories.all()],
            "languages": [language.display_name for language in source.languages.all()],
            "publishing_country": source.publishing_country.display_name,
            "readership_countries": [readership.display_name for readership in source.readership_countries.all()],
            "url": source.get_absolute_url(),
        }
        for source in readership_sources_queryset
    ]

    publishing_sources_queryset = (
        country.publishing_sources.order_by("name")
        .prefetch_related(
            Prefetch("categories", queryset=Category.objects.only("name").order_by("name")),
            Prefetch("languages", queryset=Language.objects.only("display_name", "alphanum_name").order_by("display_name")),
            Prefetch("readership_countries", queryset=Country.objects.only("display_name", "alphanum_name").order_by("display_name"),),
        )
        .select_related("publishing_country")
        .only("name", "categories", "languages", "publishing_country", "readership_countries")
    )

    publishing_sources = [
        {
            "name": source.name,
            "categories": [category.name for category in source.categories.all()],
            "languages": [language.display_name for language in source.languages.all()],
            "publishing_country": source.publishing_country.display_name,
            "readership_countries": [readership.display_name for readership in source.readership_countries.all()],
            "url": source.get_absolute_url(),
        }
        for source in publishing_sources_queryset
    ]

    return render(
        request,
        "general/view_country_detail.html",
        {"country": country, "readership_sources": readership_sources, "publishing_sources": publishing_sources},
    )


def view_language_sources(request, alphanum_name):

    language = get_object_or_404(Language, alphanum_name=alphanum_name)

    sources_queryset = (
        language.sources.order_by("name")
        .prefetch_related(
            Prefetch("categories", queryset=Category.objects.only("name").order_by("name")),
            Prefetch("readership_countries", queryset=Country.objects.only("display_name", "alphanum_name").order_by("display_name"),),
            Prefetch("languages", queryset=Language.objects.only("display_name", "alphanum_name").order_by("display_name")),
        )
        .select_related("publishing_country")
        .only("name", "categories", "languages", "publishing_country", "readership_countries")
    )

    sources = [
        {
            "name": source.name,
            "categories": [category.name for category in source.categories.all()],
            "languages": [language.display_name for language in source.languages.all()],
            "publishing_country": source.publishing_country.display_name,
            "readership_countries": [readership.display_name for readership in source.readership_countries.all()],
            "url": source.get_absolute_url(),
        }
        for source in sources_queryset
    ]

    return render(request, "general/view_language_detail.html", {"language": language, "sources": sources})


# ========================================================================================= #
#                                                                                           #
#  ██████╗`███████╗██╗`````███████╗████████╗███████╗````██████╗``██████╗`███████╗████████╗  #
#  ██╔══██╗██╔════╝██║`````██╔════╝╚══██╔══╝██╔════╝````██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝  #
#  ██║``██║█████╗``██║`````█████╗`````██║```█████╗``````██████╔╝██║```██║███████╗```██║```  #
#  ██║``██║██╔══╝``██║`````██╔══╝`````██║```██╔══╝``````██╔═══╝`██║```██║╚════██║```██║```  #
#  ██████╔╝███████╗███████╗███████╗```██║```███████╗````██║`````╚██████╔╝███████║```██║```  #
#  ╚═════╝`╚══════╝╚══════╝╚══════╝```╚═╝```╚══════╝````╚═╝``````╚═════╝`╚══════╝```╚═╝```  #
#  ```````````````````````````````````````````````````````````````````````````````````````  #
# ========================================================================================= #


@login_required()
def delete_post(request):

    if request.method != "POST":
        return HttpResponseBadRequest("Unsupported Request Method")

    pk = request.POST["post_pk"]
    post = get_object_or_404(Post, pk=pk)

    if post.author.id == request.user.id:
        post.delete()
        messages.info(request, "Post Removed")
        return redirect("index")
    else:
        messages.error(request, "Action Not Authorized")
        return redirect("view_post", pk=pk)


# ==================================================================================================== #
#                                                                                                      #
#  ███╗```██╗███████╗██╗````██╗`````██████╗`██████╗`███╗```███╗███╗```███╗███████╗███╗```██╗████████╗  #
#  ████╗``██║██╔════╝██║````██║````██╔════╝██╔═══██╗████╗`████║████╗`████║██╔════╝████╗``██║╚══██╔══╝  #
#  ██╔██╗`██║█████╗``██║`█╗`██║````██║`````██║```██║██╔████╔██║██╔████╔██║█████╗``██╔██╗`██║```██║```  #
#  ██║╚██╗██║██╔══╝``██║███╗██║````██║`````██║```██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝``██║╚██╗██║```██║```  #
#  ██║`╚████║███████╗╚███╔███╔╝````╚██████╗╚██████╔╝██║`╚═╝`██║██║`╚═╝`██║███████╗██║`╚████║```██║```  #
#  ╚═╝``╚═══╝╚══════╝`╚══╝╚══╝``````╚═════╝`╚═════╝`╚═╝`````╚═╝╚═╝`````╚═╝╚══════╝╚═╝``╚═══╝```╚═╝```  #
#  ``````````````````````````````````````````````````````````````````````````````````````````````````  #
# ==================================================================================================== #


@login_required()
def new_comment(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == "GET":
        form = NewCommentForm()
        return render(request, "general/new_comment.html", {"post": post, "form": form})
    elif request.method == "POST":
        # c_post = Post.objects.get(pk=post_pk)
        comment_body = request.POST.get("body")
        comment_author = get_user_model().objects.get(pk=request.user.pk)
        comment = Comment.objects.create(post=post, body=comment_body, author=comment_author)
        comment.save()
        return redirect("view_comment", comment.pk)
    else:
        return HttpResponseBadRequest("Unsupported Request Method")


# ====================================================================================================== #
#                                                                                                        #
#  ██╗```██╗██╗███████╗██╗````██╗`````██████╗`██████╗`███╗```███╗███╗```███╗███████╗███╗```██╗████████╗  #
#  ██║```██║██║██╔════╝██║````██║````██╔════╝██╔═══██╗████╗`████║████╗`████║██╔════╝████╗``██║╚══██╔══╝  #
#  ██║```██║██║█████╗``██║`█╗`██║````██║`````██║```██║██╔████╔██║██╔████╔██║█████╗``██╔██╗`██║```██║```  #
#  ╚██╗`██╔╝██║██╔══╝``██║███╗██║````██║`````██║```██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝``██║╚██╗██║```██║```  #
#  `╚████╔╝`██║███████╗╚███╔███╔╝````╚██████╗╚██████╔╝██║`╚═╝`██║██║`╚═╝`██║███████╗██║`╚████║```██║```  #
#  ``╚═══╝``╚═╝╚══════╝`╚══╝╚══╝``````╚═════╝`╚═════╝`╚═╝`````╚═╝╚═╝`````╚═╝╚══════╝╚═╝``╚═══╝```╚═╝```  #
#  ````````````````````````````````````````````````````````````````````````````````````````````````````  #
# ====================================================================================================== #


@login_required()
def view_comment(request, comment_pk):
    try:
        comment = Comment.objects.get(pk=comment_pk)
        return render(request, "general/view_comment.html", {"comment": comment})
    except Comment.DoesNotExist:
        raise Http404("Comment Not Found")


# ============================================================================== #
#                                                                                #
#  ██╗```██╗██╗███████╗██╗````██╗`````██████╗██╗``██╗`██████╗`██████╗``██████╗`  #
#  ██║```██║██║██╔════╝██║````██║````██╔════╝██║``██║██╔═══██╗██╔══██╗██╔═══██╗  #
#  ██║```██║██║█████╗``██║`█╗`██║````██║`````███████║██║```██║██████╔╝██║```██║  #
#  ╚██╗`██╔╝██║██╔══╝``██║███╗██║````██║`````██╔══██║██║```██║██╔══██╗██║```██║  #
#  `╚████╔╝`██║███████╗╚███╔███╔╝````╚██████╗██║``██║╚██████╔╝██║``██║╚██████╔╝  #
#  ``╚═══╝``╚═╝╚══════╝`╚══╝╚══╝``````╚═════╝╚═╝``╚═╝`╚═════╝`╚═╝``╚═╝`╚═════╝`  #
#  ````````````````````````````````````````````````````````````````````````````  #
# ============================================================================== #


def view_choro(request: requests.request, result_pk) -> render:
    result = get_object_or_404(Result, pk=result_pk)
    return render(request, "general/view_choro.html", {"result": result})


# =============================#
#                              #
#  ██╗``██╗`██████╗``██████╗`  #
#  ██║``██║██╔═████╗██╔═████╗  #
#  ███████║██║██╔██║██║██╔██║  #
#  ╚════██║████╔╝██║████╔╝██║  #
#  `````██║╚██████╔╝╚██████╔╝  #
#  `````╚═╝`╚═════╝``╚═════╝`  #
#  ``````````````````````````  #
# ======= BAD REQUEST ======== #


def handler400(request, exception):
    return render(request=request, template_name="error/400.html", context=locals(), status=400)


# ========================#
#                         #
#  ██╗``██╗`██████╗``██╗  #
#  ██║``██║██╔═████╗███║  #
#  ███████║██║██╔██║╚██║  #
#  ╚════██║████╔╝██║`██║  #
#  `````██║╚██████╔╝`██║  #
#  `````╚═╝`╚═════╝``╚═╝  #
#  `````````````````````  #
# ===== UNAUTHORIZED ==== #


def handler401(request, exception):
    return render(request=request, template_name="error/401.html", context=locals(), status=401)


# =============================#
#                              #
#  ██╗``██╗`██████╗`██████╗`   #
#  ██║``██║██╔═████╗╚════██╗   #
#  ███████║██║██╔██║`█████╔╝   #
#  ╚════██║████╔╝██║`╚═══██╗   #
#  `````██║╚██████╔╝██████╔╝   #
#  `````╚═╝`╚═════╝`╚═════╝`   #
#  `````````````````````````   #
# ===== PERMISSION DENIED ==== #
# call: raise PermissionDenied #


def handler403(request, exception):
    return render(request=request, template_name="error/403.html", context=locals(), status=403)


# =============================#
#                              #
#  ██╗``██╗`██████╗`██╗``██╗   #
#  ██║``██║██╔═████╗██║``██║   #
#  ███████║██║██╔██║███████║   #
#  ╚════██║████╔╝██║╚════██║   #
#  `````██║╚██████╔╝`````██║   #
#  `````╚═╝`╚═════╝``````╚═╝   #
#  `````````````````````````   #
# ====== PAGE NOT FOUND =======#


def handler404(request, exception):
    context = RequestContext(request)
    return render(request=request, template_name="error/404.html", context=locals(), status=404)


# ==============================#
#                               #
#  ███████╗`██████╗``██████╗`   #
#  ██╔════╝██╔═████╗██╔═████╗   #
#  ███████╗██║██╔██║██║██╔██║   #
#  ╚════██║████╔╝██║████╔╝██║   #
#  ███████║╚██████╔╝╚██████╔╝   #
#  ╚══════╝`╚═════╝``╚═════╝`   #
#  ``````````````````````````   #
# ======= SERVER ERROR =========#


def handler500(request):
    return render(request=request, template_name="error/500.html", status=500)


# ==================================#
#                                   #
#    `█████╗`██╗```██╗██╗``██╗      #
#    ██╔══██╗██║```██║╚██╗██╔╝      #
#    ███████║██║```██║`╚███╔╝`      #
#    ██╔══██║██║```██║`██╔██╗`      #
#    ██║``██║╚██████╔╝██╔╝`██╗      #
#    ╚═╝``╚═╝`╚═════╝`╚═╝``╚═╝      #
#    `````````````````````````      #
# ==================================#


def report_error(request):
    return render(request=request, template_name="error/report.html", context=locals(), status=200)


def get_query_type(qm_focus: str) -> QueryTypeChoice or None:
    if qm_focus == "QueryTypeChoice.ALL" or "all".casefold():
        query_type = QueryTypeChoice.ALL
    elif qm_focus == "QueryTypeChoice.HDL" or "headlines".casefold():
        query_type = QueryTypeChoice.HDL
    else:
        log.error(f"query_type not found in get_query_type for qm_focus of {qm_focus}")
        query_type = None
    return query_type
