from domain.article import Article
from application.ports import NewsHandler

class NewsProcessor:
    def __init__(self, handler_chain, search_term):
        self.handler_chain = handler_chain
        self.search_term = search_term
    
    def execute(self, url: NewsHandler):
        articles = self.handler_chain.handle(url)
        for article in articles:
            article.analyze_content(self.search_term)
            
        return articles