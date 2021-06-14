import json
import os
from typing import NoReturn

import pycountry
import requests
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from requests.exceptions import MissingSchema

from mtn_django.logger import log
from mtn_web.models import Article


class GeoDataManager:
    def __init__(self, req_data=None, json_data=None, result_dict=None):
        self.filename = "geo_data.txt"
        self.req_data = req_data
        self.json_data = json_data
        self.result_dict = {} if result_dict is None else result_dict
        # TODO self.result_map = {} if result_map is None else result_map

    def verify_geo_data(self) -> bool:
        have_geo = self.check_geo_data()
        if have_geo:
            self.initialize_result_dict()
            return True
        return False

    def check_geo_data(self) -> bool:
        if self.json_data is None:
            have_geo_data = self.get_geo_data()
            have_cyprus_fix = self.fix_cyprus_country_code()
            return bool(have_geo_data and have_cyprus_fix)

    def get_geo_data(self) -> bool:
        try:
            if "ON_HEROKU" in os.environ:
                geo_data_url = staticfiles_storage.url("js/geo_data.json")
                response = requests.get(geo_data_url)
                self.json_data = response.json()
                return True
            else:
                with open("mtn_web/static/js/geo_data.json") as geo_data_json:
                    self.json_data = json.load(geo_data_json)
                    if self.json_data is None:
                        raise FileNotFoundError
                return True
            return False
        except (FileNotFoundError, TypeError, IOError, MissingSchema):
            try:
                self.req_data = requests.get(os.getenv("GEO_DATA_URL"))
                if self.req_data.status_code == 200:
                    self.json_data = self.req_data.json()
                    return True
                else:
                    return False
            except requests.exceptions.RequestException as e:
                log.error(f"Error fetching mapping json: {e}")
                return False

    def fix_cyprus_country_code(self) -> bool:
        for dikt in self.json_data["features"]:
            if dikt["id"] == "-99":
                dikt["id"] = "CYP"
        return True

    def initialize_result_dict(self) -> NoReturn:
        self.result_dict = dict.fromkeys([k["id"] for k in self.json_data["features"]], 0)
        self.result_dict["SGP"] = 0
        self.result_dict["HKG"] = 0

    def add_result(self, a3_code: str) -> NoReturn:
        self.result_dict[a3_code] += 1

    # def add_result_2(self, article: Article):
    #     alpha3 = article.source_country
    #     alpha2 = pycountry.countries.get(alpha_3=alpha3))).alpha_2
    #     display_name = pycountry.countries.get(alpha_2=alpha2).name
    #     if alpha3 in self.result_map.keys():
    #         self.result_map[alpha3]['articles'].append(article.pk)
    #     else:
    #         self.result_map[alpha3]['articles'] = [article.pk]
    #         self.result_map[alpha3]['alpha2'] = alpha2
    #         self.result_map[alpha3]['display_name'] = display_name
    # TODO implement above and use len of list to get total article count and list of article pks

    def json_to_file(self) -> bool:
        with open(self.filename, "w") as outfile:

            json.dump(self.json_data, outfile)
            return True
