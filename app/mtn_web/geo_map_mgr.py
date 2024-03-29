import os
from datetime import datetime

import branca
import folium
import geopandas as gp
import numpy as np
import pandas as pd
import pycountry
from mtn_django.logger import log
from mtn_web.geo_data_mgr import GeoDataManager
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from folium import ColorMap as cm

import shapely
import warnings
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

CHORO_MAP_ROOT = os.path.join(settings.BASE_DIR, "Choropleth_")


class GeoMapManager:
    # TODO move map_source in to Source Model as alpha2_to_alpha3(alpha2_code: str):
    @staticmethod
    def map_source(source_country):
        return (pycountry.countries.get(alpha_2=str(source_country).upper())).alpha_3 if source_country else None

    def build_choropleth(self, argument, focus, geo_data_manager: GeoDataManager) -> (folium.Map, str) or None:

        try:
            world_df = gp.read_file("mtn_web/static/js/geo_data.json")
            global_map = folium.Map(location=[0, 0], tiles="OpenStreetMap", zoom_start=3)
            articles_per_country = pd.Series(geo_data_manager.result_dict)
            world_df["article_count"] = world_df["id"].map(articles_per_country)
            world_df.head()
            world_df.plot(column="article_count")
            threshold_scale = self.get_threshold(articles_per_country)
            folium.Choropleth(
                geo_data=geo_data_manager.json_data,
                name="choropleth",
                data=world_df,
                columns=["id", "article_count"],
                key_on="feature.id",
                fill_color="Dark2_r",
                bins=[float(x) for x in threshold_scale],  # https://github.com/python-visualization/folium/issues/1130
                fill_opacity=0.8,
                line_opacity=0.2,
                nan_fill_color="#1a2b29",
                nan_fill_opacity=0.7,
                highlight=True,
            ).add_to(global_map)
            # ----------------------------------------------------------#
            #             Alternative fill_color options                #
            # ----------------------------------------------------------#
            #    YlGrBu - RdYlGn - YlOrBr - RdYlBu - PuBuGn - YlOrRd    #
            #     Oranges - Greens -Purples - Reds - Greys - Blues      #
            # Pastel1 - Pastel2 - Spectral - Set1 - Set2 - Set3 - Dark2 #
            # ----------------------------------------------------------#
            #  TODO offer fill color options for user selection
            folium.TileLayer("stamenwatercolor", attr="attr").add_to(global_map)
            folium.TileLayer("stamenterrain", attr="attr").add_to(global_map)
            folium.TileLayer("cartodbpositron", attr="attr").add_to(global_map)
            folium.TileLayer("OpenStreetMap", attr="attr").add_to(global_map)
            folium.LayerControl().add_to(global_map)
            filename = f"{datetime.ctime(datetime.now()).replace(' ', '_').replace(':', '-')}_{focus}_query_{argument}_choropleth_map.html"
            global_map.save(CHORO_MAP_ROOT + filename)  # TODO offer user download of map html file
            return global_map, filename if global_map and filename else None

        except FileNotFoundError as e:
            log.error(f"Error fetching mapping json: {e}")
            return None

    @staticmethod
    def get_threshold(articles_per_country: [dict]) -> [int]:
        if articles_per_country.values.max() <= 5:
            threshold_scale = [0, 1, 2, 3, 4, 5]
        elif 5 < articles_per_country.values.max() <= 16:
            # threshold_scale = np.linspace(
            #     articles_per_country.values.min(),
            #     articles_per_country.values.max() + 1,
            #     6,
            #     dtype=int,
            # ).tolist()
            threshold_scale = [0, 1].append(np.linspace(2, articles_per_country.values.max() + 1, 4).to_list())
        elif 160 >= articles_per_country.values.max() > 16:

            threshold_scale = [0, 1, 3, 7, 15, articles_per_country.values.max() + 1]
        elif articles_per_country.values.max > 160:
            threshold_scale = [0, 1, 5, 13, 29, articles_per_country.values.max() + 1]
        else:
            log.error("threshold-scale not being set in choropleth by articles_per_country.max")
            threshold_scale = [0, 1, 2, 3, 4, 5]
        return threshold_scale

    @staticmethod
    def choro_to_file(choro_html: str, filename: str) -> bool:
        try:
            with open(CHORO_MAP_ROOT + filename, "w") as file:
                file.write(choro_html)
                return True
        except FileNotFoundError as e:
            log.error(f"Error writing choropleth HTML to file: {e}")
            return False
