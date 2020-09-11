import json
import os
import random
from http import HTTPStatus

import requests
import pycountry
from django.templatetags.static import static
from django.db import IntegrityError

from mtn_django.logger import log
from mtn_web.models import Category, Source, Language, Country

from .data import api_country_codes, categories, country_codes

api_key = os.getenv("MTN_SIFTER_API_KEY")


def sift():
    rand_country, rand_category = get_random_targets()
    country_src_data = req_country_src_data(
        alpha2_iso_code=rand_country, src_cat=rand_category
    )
    if country_src_data is not None:
        log.info(f'Sift(): (src_data={country_src_data[:200]})  (alpha2_iso_code={rand_country})  (src_cat={rand_category})')
        build_country_src_data(
            src_data=country_src_data, alpha2_iso_code=rand_country, src_cat=rand_category
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
                    # language, created = Language.objects.get_or_create(alpha2_code=src['language'])
                    language = get_or_create_language(src['language'])
                    country = get_or_create_country(src['country'])
                    if language and country:
                        new_src = Source.objects.create(
                            name=src["name"],
                            publishing_country=country,
                            url=src["url"],
                        )
                    new_src.categories.add(cat)            
                    new_src.languages.add(language)
                return True
        except FileNotFoundError:
            log.info("Unable to find file for building base sources.")
            src_data = req_top_src_data()
            if src_data:
                build_top_src_data(src_data)
                return True
            else:
                return False


def get_or_create_language(alpha2_code):

    try:
        language_full_name = pycountry.languages.get(alpha_2=alpha2_code).name
        display_name = language_full_name
        alphanum_filter = filter(str.isalnum, language_full_name)
        alphanum_name = "".join(alphanum_filter)
    except LookupError:
        display_name = alpha2_code
        alphanum_name = alpha2_code
    try:
        language, created = Language.objects.get_or_create(
            alpha2_code=alpha2_code,
            display_name=display_name,
            alphanum_name=alphanum_name
        )
    except IntegrityError as e:
        log.warning(f'Attempt to add already present Language to database: {e}')
        language = False
    except Language.MultipleObjectsReturned as e:
        log.warning(f'get_or_create retrieved multiple results: {e}')
        language = False
    return language


def get_or_create_country(alpha2_code):

    try:
        country_full_name = pycountry.countries.lookup(alpha2_code).name
        comma_index = country_full_name.find(',')
        if comma_index == -1:  # No comma in full_country_name
            display_name = country_full_name
        else:
            '''
                Substring up to first comma, i.e. "Bolivia, Plurinational State of" will return "Bolivia".
                This is dont as the country names are used to:
                    - generate element id's in templates, and neither spaces or commas are allowed.
                    - As a user-friendly alternative to being presented iso-alpha2/3 codes in templates.
            '''
            display_name = country_full_name[:comma_index]
        alphanum_filter = filter(str.isalnum, country_full_name)
        alphanum_name = "".join(alphanum_filter)
    except LookupError:
        display_name = country_full_name
        alphanum_name = alpha2_code
    try:
        country, created = Country.objects.get_or_create(
            alpha2_code=alpha2_code,
            display_name=display_name,
            alphanum_name=alphanum_name
        )
    except IntegrityError as e:
        log.warning(f'Attempt to add already present Country to database: {e}')
        country = False
    except Country.MultipleObjectsReturned as e:
        log.warning(f'get_or_create retrieved multiple results: {e}')
        country = False
    return country


def get_random_targets():
    countries = list(api_country_codes.keys())
    rand_country = random.choice(countries)
    rand_category = random.choice(categories)
    return rand_country, rand_category


def req_country_src_data(alpha2_iso_code, src_cat=None):
    if src_cat is None:
        endpoint = f"https://newsapi.org/v2/top-headlines?country={alpha2_iso_code}&apiKey={api_key}"
    else:
        endpoint = f"https://newsapi.org/v2/top-headlines?country={alpha2_iso_code}&category={src_cat}&apiKey={api_key}"
    try:
        response = requests.get(endpoint)
        if response.status_code == HTTPStatus.OK:
            return response.json()["articles"]
        else:
            response.raise_for_status()
            # TODO msg/log
            return None
    except requests.exceptions.HTTPError as err:
        log.error(f"{err} in req_country_src_data({alpha2_iso_code}, {src_cat})")
        return None


def build_country_src_data(src_data, alpha2_iso_code, src_cat):
    cat, created = Category.objects.get_or_create(name=src_cat)
    for article in src_data:
        src = check_for_source(article["source"]["name"])
        language_alpha2 = api_country_codes.get(alpha2_iso_code).get('language')
        language = get_or_create_language(language_alpha2)
        country = get_or_create_country(alpha2_iso_code)
        if src is None:
            if country and language:
                new_src = Source.objects.create(
                    name=article["source"]["name"],
                    publishing_country=country
                )
                new_src.languages.add(language)
                new_src.categories.add(cat)
        elif type(src) is Source:
            src.categories.add(cat)
            src.languages.add(language)
            if src.publishing_country is not country:
                src.readership_countries.add(country)
        else:
            log.error(f'{type(src)} passed when expecting {type(Source)} or type{None} ')
    return


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
        log.error(f"{err} in req_top_src_data()")
        return None


def build_top_src_data(src_data):
    for src in src_data:
        cat, created = Category.objects.get_or_create(name=src["category"])
        source = check_for_source(src["name"])
        language = get_or_create_language(src['language'])
        country = get_or_create_country(src['country'])
        if language and country:
            if source is None:
                new_src = Source.objects.create(
                    name=src["name"],
                    publishing_country=country,          
                    url=src["url"],
                )    
                new_src.categories.add(cat)
                new_src.languages.add(language)
            elif type(source) is Source:       
                source.categories.add(cat)
                source.languages.add(language)
                if source.publishing_country is not country:
                    source.readership_countries.add(country)
            else:
                log.warning('Unexpected type returned from check_for_source()')
        else:
            log.info(f'get_or_create failed for one or more value:\n    language: {src["language"]}\n    country: {src["country"]}')
    return True


def check_for_source(src_name: str) -> Source or None:
    if src_name:
        try:
            return Source.objects.get(name=src_name)
        except (AttributeError, Source.DoesNotExist) as err:
            log.error(f"{err} in check_for_source({src_name})")
            return None
    else:
        return None
