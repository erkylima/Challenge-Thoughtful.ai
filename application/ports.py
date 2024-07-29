from abc import ABC, abstractmethod
from domain.article import NewsArticle

class NewsHandler(ABC):
    @abstractmethod
    def handle(self, articles: list[NewsArticle], url:str, search_phrase:str):
        pass