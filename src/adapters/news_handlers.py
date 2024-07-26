from application.use_cases import NewsHandler
from RPA.Browser.Selenium import Selenium
from domain.article import NewsArticle

class BaseHandler(NewsHandler):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, url):
        if self.next_handler:
            return self.next_handler.handle(url)
        return []

class LATimesNewsHandler(BaseHandler):
    def __init__(self, next_handler=None):
        super().__init__(next_handler)
        self.browser = Selenium()
    
    def handle(self,url):
        self.browser.open_browser(url=url)
        titles = self.browser.find_elements_by_css_selector(".article-headline a")
        articles = []
        for title in titles:
            articles.append(NewsArticle(title.text, "", "", ""))
        return articles
