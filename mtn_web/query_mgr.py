import logging
import os
from datetime import datetime, timedelta
import requests
from newsapi import NewsApiClient

logger = logging.getLogger(__name__)
api_key = os.environ.get('NEWS_API_KEY_2')
news_api = NewsApiClient(api_key=api_key)


class Query:

    def __init__(self, arg: str, focus: str, from_date: datetime = None, to_date: datetime = None, endpoint: str = None):
        self.arg = arg
        self.focus = focus
        self.from_date = from_date
        self.to_date = to_date
        self.endpoint = endpoint

    @property
    def filename(self) -> str:
        date_created = datetime.now().strftime('%Y%m%d-%H%M%S')
        return f'api_data-{self.arg}_{self.focus}-{date_created}.json'

    def validate_date_range(self) -> bool:
        has_range =  self.to_date - self.from_date >= timedelta(0)
        is_past = datetime.now() - self.to_date >= timedelta(0)
        return has_range and is_past

    def get_endpoint(self) -> bool:
        valid_date_range = self.validate_date_range() if self.from_date and self.to_date else False
        if valid_date_range:
            if self.focus == 'all':
                self.endpoint = f'https://newsapi.org/v2/everything?q={self.arg}&from={self.from_date}&to={self.to_date}&apiKey={api_key}&pageSize=100'
            elif self.focus == 'headlines':
                self.endpoint = 'b'
            else:
                self.endpoint = 'c'
                return False
        else:
            if self.focus == 'all':
                self.endpoint = f'https://newsapi.org/v2/everything?q={self.arg}&apiKey={api_key}&pageSize=100'
            elif self.focus == 'headlines':
                self.endpoint = f'https://newsapi.org/v2/top-headlines?q={self.arg}&apiKey={api_key}&pageSize=100'
            else:
                self.endpoint = None
                return False
        return True

    def execute_query(self) -> ([dict], int):
        response = requests.get(self.endpoint)
        article_count = int(response.json()['totalResults'])
        response_data = response.json()['articles']
        article_data = []
        article_data.extend(response_data)

        # ********************* FREE VERSION OF NEWS_API LIMITS RESULTS TO 100 PER REQUEST, BELOW IS FOR PAGING THROUGH MORE THAN 100 RESULTS *****************
        #
        # if article_count > 100:
        #     pages = article_count//100
        #     if pages > 5:
        #         pages = 5
        #
        #     for p in range(2, pages+2):  # 1st page processed already, +2 to account for exclusive range and remainder
        #         try:
        #             page = requests.get(f'{self.endpoint}&page={p}')
        #             print(f'len(page.json()[articles])={len(page.json()["articles"])}')
        #             article_data.extend(page.json()['articles'])
        #
        #         except requests.exceptions.RequestException as rE:
        #             logger.log(level=logging.INFO, msg=f'RequestException while getting article_data @ page # {p}')
        #             logger.log(level=logging.ERROR, msg=logger.exception(rE))
        #             continue
        #
        #         except builtins.KeyError as kE:
        #             logger.log(level=logging.INFO, msg=f'KeyErrorException while getting article_data on {p}')
        #             logger.log(level=logging.ERROR, msg=logger.exception(kE))
        #             continue
        #     print(f'len(article data)={len(article_data)} pages={pages} article_count={article_count}')

        return article_data, article_count

    def to_file(self, data) -> bool:
        try:
            with open(self.filename, 'w+') as file:
                file.write(str(data))
            return True
        except UnicodeEncodeError:
            logger.exception(UnicodeEncodeError, 'UnicodeEncodeError during writing articles.json to file (QueryManager)')
            return False
        except AttributeError:
            logger.exception(AttributeError, 'AttributeException during writing articles.json to file (QueryManager)')
            return False
        except TypeError:
            logger.exception(TypeError, 'TypeError while ')
            return False
