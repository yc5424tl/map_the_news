import os
from datetime import datetime
from dateutil.parser import parse
from app.mtn_web.models import Article, Result, Source
from app.mtn_django.logger import log

api_key = os.getenv("MTN_WEB_API_KEY")


class Constructor:
    def new_article(self, api_response: dict, result: Result) -> Article or False:

        source = self.verify_source(api_response["source"]["name"])
        date_published = self.verify_date(api_response["publishedAt"])
        description = None

        if source:
            description = self.get_article_description(api_response)
            title = self.get_article_title(api_response)
            author = self.get_article_author(api_response)

            article_url = api_response["url"]
            image_url = api_response["urlToImage"] if api_response["urlToImage"] is not None else None
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

    def get_article_description(self, api_response):
        description = "Unavailable"
        try:
            if api_response["description"] is not None:
                if self.verify_str(api_response["description"]):
                    description = self.verify_str(api_response["description"])
                    if description == "":
                        try:
                            content = api_response["content"][:2500]
                            if content is not None and content != "":
                                description = content
                        except UnicodeDecodeError as e:
                            log.debug(f"UnicodeDecodeError while parsing content for new article: {e}\nSource Data: {api_response}")
                        except KeyError as e:
                            log.debug(f"KeyError while parsing content for new article: {e}\nSource Data: {api_response}")
        except UnicodeDecodeError as e:
            log.debug(f"UnicodeDecodeError while parsing description for new article: {e}\nSource Data: {api_response}")
        return description

    def get_article_author(self, api_response):
        author = "Unavailable"
        try:
            if self.verify_str(api_response["author"]) is not None:
                author = self.verify_str(api_response["author"])
        except UnicodeEncodeError as e:
            log.debug(f"UnicodeDecodeError while parsing author for new article: {e}\nSource Data {e}")
        return author

    def get_article_title(self, api_response):
        title = "Unavailable"
        try:
            if self.verify_str(api_response["title"]) is not None:
                title = self.verify_str(api_response["title"])
        except UnicodeDecodeError as e:
            log.debug(f"UnicodeDecodeError while parsing title for new article: {e}\nSource Data {e}",)
        return title

    def build_article_data(self, article_data_list: [{}], query_result: Result) -> [Article]:
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
    def format_date(data) -> datetime or None:
        try:
            return parse(data)
        except ValueError:
            return None

    @staticmethod
    def verify_source(source_name: str) -> str or False:
        if source_name:
            try:
                source = Source.objects.get(name=source_name)
            except (AttributeError, Source.DoesNotExist) as e:
                log.error(f"{e} propagating from constructor.verify_source({source_name})")
                source = False
        else:
            log.error(f"{source_name} retrieval failed.")
            source = False
        return source
