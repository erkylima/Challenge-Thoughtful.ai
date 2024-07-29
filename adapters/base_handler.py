from application.ports import NewsHandler
from domain.article import NewsArticle

class BaseHandler(NewsHandler):
    def __init__(self, next_handler:NewsHandler=None):
        self.next_handler = next_handler

    def handle(self, articles: list[NewsArticle], url: str, 
               search_phrase: str, filters: str, months: int):
        if self.next_handler:
            articles = self.next_handler.handle(articles, url,
                                                search_phrase, filters,
                                                months)
        return articles