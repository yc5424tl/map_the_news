from mtn_web.models import Source, Category

from .data import api_country_codes, categories, country_codes
import random
import os
import requests
from http import HTTPStatus
import logging
from django.templatetags.static import static
import json


logger = logging.getLogger(__name__)
api_key = os.getenv("SIFTER_API_KEY")


def sift():
    rand_country, rand_category = get_random_targets()
    country_src_data = req_country_src_data(
        alpha2_code=rand_country, src_cat=rand_category
    )
    if country_src_data is not None:
        build_country_src_data(
            src_data=country_src_data, alpha2_code=rand_country, src_cat=rand_category
        )
    return True


def verify_base_cat():
    for cat in categories:
        Category.objects.get_or_create(name=cat)
    return True


def verify_base_src():
    try:
        Source.objects.get(id=1)
        return True
    except (AttributeError, Source.DoesNotExist):
        try:
            with open(static("json/top_sources.json")) as json_data:
                src_data = json.load(json_data)["sources"]
                for src in src_data:
                    cat, created = Category.objects.get_or_create(name=src["category"])
                    new_src = Source.objects.create(
                        name=src["name"],
                        country=src["country"],
                        language=src["language"],
                        url=src["url"],
                    )
                    new_src.categories.add(cat)
                    new_src.save()
                return True
        except FileNotFoundError:
            logger.log(
                level=logging.INFO, msg="Unable to find file for building base sources."
            )
            src_data = req_top_src_data()
            if src_data:
                build_top_src_data(src_data)
                # scheduler.pause()
                # t = Timer(360.0, scheduler.resume())
                # t.start()
                return True
            else:
                return False


def get_random_targets():
    countries = list(api_country_codes.keys())
    rand_country = random.choice(countries)
    rand_category = random.choice(categories)
    return rand_country, rand_category


def req_country_src_data(alpha2_code, src_cat=None):
    if src_cat is None:
        endpoint = f"https://newsapi.org/v2/top-headlines?country={alpha2_code}&apiKey={api_key}"
    else:
        endpoint = f"https://newsapi.org/v2/top-headlines?country={alpha2_code}&category={src_cat}&apiKey={api_key}"
    try:
        response = requests.get(endpoint)
        if response.status_code == HTTPStatus.OK:
            return response.json()["articles"]
        else:
            response.raise_for_status()
            # TODO msg/log
            return None
    except requests.exceptions.HTTPError as err:
        logger.log(
            level=logging.ERROR,
            msg=f"{err} in req_country_src_data({alpha2_code}, {src_cat})",
        )
        return None


def build_country_src_data(src_data, alpha2_code, src_cat):
    cat, created = Category.objects.get_or_create(name=src_cat)
    for article in src_data:
        src = check_for_source(article["source"]["name"])
        if src is None:
            new_src = Source.objects.create(
                name=article["source"]["name"],
                country=alpha2_code,
                language=api_country_codes.get(alpha2_code).get("language"),
            )
            new_src.categories.add(cat)
            new_src.save()
        else:
            if cat not in src.categories.all():
                src.categories.add(cat)
                src.save()
    return True


def req_top_src_data():
    response = requests.get(f"https://newsapi.org/v2/sources?apiKey={api_key}")
    try:
        if response.status_code == HTTPStatus.OK:
            return response.json()["sources"]
        else:
            response.raise_for_status()
            # TODO msg/log
            return None
    except requests.exceptions.HTTPError as err:
        logger.log(level=logging.ERROR, msg=f"{err} in req_top_src_data()")
        return None


def build_top_src_data(src_data):
    for src in src_data:
        cat, created = Category.objects.get_or_create(name=src["category"])
        if created:
            cat.save()
        source = check_for_source(src["name"])
        if source is None:
            new_src = Source.objects.create(
                name=src["name"],
                country=src["country"],
                language=src["language"],
                url=src["url"],
            )
            new_src.categories.add(cat)
            new_src.save()
        else:
            if cat not in src.categories.all():
                src.categories.add(cat)
                src.save()
    return True


def check_for_source(src_name: str) -> Source or None:
    if src_name:
        try:
            return Source.objects.get(name=src_name)
        except (AttributeError, Source.DoesNotExist) as err:
            logger.log(
                level=logging.ERROR, msg=f"{err} in check_for_source({src_name})"
            )
            return None
    else:
        return None
