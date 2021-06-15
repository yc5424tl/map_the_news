import os
from datetime import datetime, timedelta

import requests
from mtn_django.logger import log
from mtn_web.models import QueryTypeChoice
from newsapi import NewsApiClient

api_key = os.environ.get("MTN_WEB_API_KEY")
news_api = NewsApiClient(api_key=api_key)


class Query:
    def __init__(
        self, arg: str, focus: QueryTypeChoice, from_date: datetime = None, to_date: datetime = None, endpoint: str = None,
    ):
        self.arg = arg
        self.focus = focus
        self.from_date = from_date
        self.to_date = to_date
        self.endpoint = endpoint

    @property
    def filename(self) -> str:
        date_created = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"api_data-{self.arg}_{self.focus}-{date_created}.json"

    def validate_date_range(self) -> bool:
        has_range = self.to_date - self.from_date >= timedelta(0)
        is_past = datetime.now() - self.to_date >= timedelta(0)
        return has_range and is_past

    def get_endpoint(self) -> bool:
        if self.focus == QueryTypeChoice.ALL:
            self.endpoint = f"https://newsapi.org/v2/everything?q={self.arg}&apiKey={api_key}&pageSize=100"
        elif self.focus == QueryTypeChoice.HDL:
            self.endpoint = f"https://newsapi.org/v2/top-headlines?q={self.arg}&apiKey={api_key}&pageSize=100"
        else:
            self.endpoint = None
            print (self.endpoint)
            return False

        return True

    def execute_query(self) -> ([dict], int):
        response = requests.get(self.endpoint)
        print(response.json())
        if response.json()["status"] == "error":
            print(response.json())
            log.error(response.json())
            err_code = response.json()["status"]["code"]
            return False, False
        log.info(f"response = \n\n{response}")
        article_count = int(response.json()["totalResults"])
        response_data = response.json()["articles"]
        article_data = list(response_data)

        # ** DO NOT UNCOMMENT CODE BELOW UNLESS YOU HAVE A PAID SUBSCRIPTION FOR NEWSAPI
        # free version is limited to first 100 results (cannot use multiple requests to page results),
        # you will burn up your api calls fast fast fast if using the below w/ free api
        # BELOW IS FOR PAGING THROUGH MORE THAN 100 RESULTS**
        """
        if article_count > 100:
            pages = article_count//100
            if pages > 5:
                pages = 5

            for p in range(2, pages+2):  # 1st page processed already, +2 to account for exclusive range and the remaining page of <100 articles left after floor division
                try:
                    page = requests.get(f'{self.endpoint}&page={p}')
                    print(f'len(page.json()[articles])={len(page.json()["articles"])}')
                    article_data.extend(page.json()['articles'])

                except requests.exceptions.RequestException as rE:
                    logger.log(level=logging.INFO, msg=f'RequestException while getting article_data @ page # {p}')
                    logger.log(level=logging.ERROR, msg=logger.exception(rE))
                    continue

                except builtins.KeyError as kE:
                    logger.log(level=logging.INFO, msg=f'KeyErrorException while getting article_data on {p}')
                    logger.log(level=logging.ERROR, msg=logger.exception(kE))
                    continue
        """
        return article_data, article_count
