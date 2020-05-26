import json
import logging
from typing import NoReturn
import requests
from django.templatetags.static import static
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
            # have_json = self.json_to_file()
            # if have_json:
            self.initialize_result_dict()
            return True
        return False

    def check_geo_data(self) -> bool:
        if self.json_data is None:
            have_geo_data = self.get_geo_data()
            have_cyprus_fix = self.fix_cyprus_country_code()
            if have_geo_data and have_cyprus_fix:
                return True
            else:
                return False

    def get_geo_data(self) -> bool:
        try:
            geo_data_url = staticfiles_storage.url('js/geo_data.json')
            response = requests.get(geo_data_url)
            geo_data_json = response.json()
            print(f'geo_data_json type={type(geo_data_json)} value=>\n{geo_data_json}\n\n')
            # with open(static("js/geo_data.json")) as json_file:
            self.json_data = geo_data_json
            print('have self.json_data from static')
            return True
        except FileNotFoundError:
            try:
                self.req_data = requests.get(
                    "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
                )
                if self.req_data.status_code == 200:
                    self.json_data = self.req_data.json()
                    print('have self.json_data from request')
                    return True
                else:
                    return False
            except requests.exceptions.RequestException as e:
                logger.log(level=logging.ERROR, msg=f"Error fetching mapping json: {e}")
                return False

    def fix_cyprus_country_code(self) -> bool:
        # print(f'type(self.json_data) = {type(self.json_data)}')
        # print(f'\n\nself.json_data =====>\n{self.json_data}\n\n')
        # as_dict = json.loads(self.json_data)
        # print(f'type(as_dict) == {type(as_dict)}')
        # print('\n\nas_dict ======>\n{as_dict}\n\n')
        # for key in as_dict:
        #     if self.json_data[key] == "-99":
        #         self.json_data[key] = "CYP"
        for dict in self.json_data['features']:
            if dict['id'] == '-99':
                dict['id'] = 'CYP'
        return True

    def initialize_result_dict(self) -> NoReturn:
        self.result_dict = dict.fromkeys(
            [k["id"] for k in self.json_data["features"]], 0
            # [k["id"] for k in json.loads(self.json_data)["features"]], 0
        )
        # try:
        #     # print('opening file in initialize result dict')
        #     # with open(static('js/geo_data.txt')) as file:
        #     geo_data_url = staticfiles_storage.url('js/geo_data.txt')
        #     response = requests.get(geo_data_url)
        #     geo_data_txt = response.text
        #     geo_data_json = json.loads(geo_data_txt)
        #     # json_data = json.load(geo_data)
        #     # print(f'json_data from json.load(file) = {json_data}')
        #     features = geo_data_json['features']
        #     # print(f'features from json_data = {features}')
        #     self.result_dict = dict.fromkeys(
        #         [k['id'] for k in features], 0,
        #     )
        #     # self.result_dict = dict.fromkeys(
        #     #     [
        #     #         k["id"]
        #     #         for k in json.load(open(static(f"js/{self.filename}")))["features"]
        #     #     ],
        #     #     0,
        #     # )
        # except (KeyError, FileNotFoundError):
        #     print(f'type(self.json_data) == {type(self.json_data)}')
        #     self.result_dict = dict.fromkeys(
        #         [k["id"] for k in json.loads(self.json_data)["features"]], 0
        #     )

    def add_result(self, a3_code: str) -> NoReturn:
        self.result_dict[a3_code] += 1

    # TODO look at how to create files in s3 programatically
    def json_to_file(self) -> bool:
        with open(self.filename, "w") as outfile:
            json.dump(self.json_data, outfile)
            return True
