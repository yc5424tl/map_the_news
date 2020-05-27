import logging
import os
from datetime import datetime
from dateutil.parser import parse
from mtn_web.models import Article, Result, Source

api_key = os.getenv("NEWS_API_KEY_2")
logger = logging.getLogger(__name__)


class Constructor:
    def new_article(self, api_response, result: Result) -> Article or False:
        source = self.verify_source(api_response["source"]["name"])
        date_published = self.verify_date(api_response["publishedAt"])
        try:
            description = (
                self.verify_str(api_response["description"])
                if api_response["description"] is not None
                else "Unavailable"
            )
        except UnicodeDecodeError as e:
            logger.log(
                level=logging.DEBUG,
                msg=f"UnicodeDecodeError while parsing description for new article: {e}\nSource Data: {api_response}",
            )
            description = "Unavailable"
        try:
            title = self.verify_str(api_response["title"])
            if title is None:
                title = "Unavailable"
        except UnicodeDecodeError as e:
            logger.log(
                level=logging.DEBUG,
                msg=f"UnicodeDecodeError while parsing title for new article: {e}\nSource Data {e}",
            )
            title = "Unavailable"
        try:
            author = self.verify_str(api_response["author"])
            if author is None:
                author = "Unavailable"
        except UnicodeEncodeError as e:
            logger.log(
                level=logging.DEBUG,
                msg=f"UnicodeDecodeError while parsing author for new article: {e}\nSource Data {e}",
            )
            author = "Unavailable"
        if source:
            article_url = api_response["url"]
            image_url = (
                api_response["urlToImage"]
                if api_response["urlToImage"] is not None
                else None
            )
            new_article = Article(
                article_url=article_url,
                author=author,
                date_published=date_published,
                description=description,
                image_url=image_url,
                result=result,
                source=source,
                title=title,
            )
            new_article.save()
            return new_article
        else:
            return False

    def build_article_data(
        self, article_data_list: [{}], query_result: Result
    ) -> [Article]:
        article_list = []
        for article_data in article_data_list:
            new_article = self.new_article(article_data, query_result)
            if new_article:
                article_list.append(new_article)
        return article_list

    @staticmethod
    def verify_str(data: str) -> str or None:
        if data and isinstance(data, str):
            return data
        else:
            return None

    def verify_date(self, data: datetime) -> datetime or None:
        f_data = self.format_date(data)
        if data and isinstance(f_data, datetime):
            return f_data
        else:
            return None

    @staticmethod
    def format_date(data):
        try:
            return parse(data)
        except ValueError:
            return None

    @staticmethod
    def verify_source(source_name) -> str or False:
        if source_name:
            try:
                return Source.objects.get(name=source_name)
            except (AttributeError, Source.DoesNotExist) as e:
                logger.log(
                    level=logging.ERROR,
                    msg=f"{e} propagating from constructor.verify_source({source_name})",
                )
                return False
        else:
            logger.error(f"{source_name} retrieval failed.")
            return False
