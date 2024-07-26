from adapters.news_handlers import LATimesScraperNewsHandler, ExcelSaverHandler
from application.use_cases import NewsProcessor
if __name__ == "__main__":
    handler_chain = LATimesScraperNewsHandler(ExcelSaverHandler())

    search_term = "soccer"

    news_processor = NewsProcessor(handler_chain, search_term)

    url = "https://www.latimes.com/"