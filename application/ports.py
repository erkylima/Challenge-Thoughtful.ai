from abc import ABC, abstractmethod
from domain.article import NewsArticle
from application.errors import NewsHandlerError
class NewsHandler(ABC):
    @abstractmethod
    def handle(self, articles: list[NewsArticle], url:str, search_phrase:str, filters: str, months: int):
        pass

    
    def attempt_again(self, func, max_attempts, *args):
        attempts = 0

        while attempts < max_attempts:
            try:
                return func(*args)
            except Exception as e:
                attempts += 1
                print(f"Attempt {attempts} failed. Retrying...")
                continue

        raise RuntimeError(NewsHandlerError.MAX_ATTEMPS_ERROR)