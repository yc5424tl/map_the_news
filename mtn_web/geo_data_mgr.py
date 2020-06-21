import json
import logging
from typing import NoReturn
import requests
from django.contrib.staticfiles.storage import staticfiles_storage

logger = logging.getLogger(__name__)


class GeoDataManager:
    def __init__(self, req_data=None, json_data=None, result_dict=None):
        self.filename = "geo_data.txt"
        self.req_data = req_data
        self.json_data = json_data
        self.result_dict = {} if result_dict is None else result_dict

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
            geo_data_url = staticfiles_storage.url("js/geo_data.json")
            response = requests.get(geo_data_url)
            geo_data_json = response.json()
            self.json_data = geo_data_json
            return True
        except FileNotFoundError:
            try:
                self.req_data = requests.get(
                    "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
                )
                if self.req_data.status_code == 200:
                    self.json_data = self.req_data.json()
                    return True
                else:
                    return False
            except requests.exceptions.RequestException as e:
                logger.log(level=logging.ERROR, msg=f"Error fetching mapping json: {e}")
                return False

    def fix_cyprus_country_code(self) -> bool:
        for dikt in self.json_data["features"]:
            if dikt["id"] == "-99":
                dikt["id"] = "CYP"
        return True

    def initialize_result_dict(self) -> NoReturn:
        self.result_dict = dict.fromkeys(
            [k["id"] for k in self.json_data["features"]], 0
        )
        self.result_dict["SGP"] = 0
        self.result_dict["HKG"] = 0

    def add_result(self, a3_code: str) -> NoReturn:
        self.result_dict[a3_code] += 1

    # TODO look at how to create files in s3 programatically
    def json_to_file(self) -> bool:
        with open(self.filename, "w") as outfile:
            json.dump(self.json_data, outfile)
            return True
