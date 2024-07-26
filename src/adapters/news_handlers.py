from application.use_cases import NewsHandler
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from domain.article import NewsArticle
import os

class BaseHandler(NewsHandler):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, url):
        if self.next_handler:
            return self.next_handler.handle(url)
        return []

class LATimesScraperNewsHandler(BaseHandler):
    def __init__(self, next_handler=None):
        super().__init__(next_handler)
        self.browser = Selenium()
    
    def handle(self,url):
        self.browser.open_available_browser(url=url)
        sections_button = self.browser.find_element("button", "navigation-button")
        articles = []
        # for title in titles:
        #     articles.append(NewsArticle(title.text, "", "", ""))
        return articles

    def _scrape_news(self):
        articles = []
    
    def _download_image(self, url):
        image_data = self.browser.download(url)
        file_name = os.path.join("output/images", os.path.basename(url))
        with open(file_name, "wb") as file:
            file.write(image_data)
        return file_name

class ExcelSaverHandler(BaseHandler):
    def __init__(self, next_handler=None, filename="output/news_data.xlsx"):
        super().__init__(next_handler)
        self.filename = filename
        self.excel = Files()
    
    def handle(self, url):
        articles = super().handle(url)
        self._save_to_excel(articles)
        return articles
    
    def _save_to_excel(self, articles):
        self.excel.create_workbook(self.filename)
        self.excel.create_worksheet("News")
        self.excel.append_rows_to_worksheet([["title", "date", "description", "image_name", "count_of_search", "contains_money"]])

        for article in articles:
            self.excel.append_rows_to_worksheet([[
                article.title,
                article.date,
                article.description,
                article.image_filename,
                article.search_term_count,
                article.contains_money
            ]])
        self.excel.save_workbook()