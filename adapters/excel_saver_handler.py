from adapters.base_handler import BaseHandler, NewsArticle
from RPA.Excel.Files import Files

class ExcelSaverHandler(BaseHandler):
    def __init__(self, next_handler=None, filename="output/news_data.xlsx"):
        super().__init__(next_handler)
        self.filename = filename
        self.excel = Files()
    
    def handle(self, articles: list[NewsArticle], url: str, search_phrase: str, filter: str):
        articles = super().handle(articles, url, search_phrase, filter)
        self._save_to_excel(articles)
        return articles
    
    def _save_to_excel(self, articles: list[NewsArticle]):
        self.excel.create_workbook(self.filename)
        self.excel.rename_worksheet("Sheet", "News")
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