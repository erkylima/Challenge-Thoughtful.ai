from abc import ABC, abstractmethod

class NewsHandler(ABC):
    @abstractmethod
    def handle(self, url):
        pass