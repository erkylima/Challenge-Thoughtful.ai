from adapters.la_times_scraper_handler import LATimesScraperNewsHandler
from adapters.excel_saver_handler import ExcelSaverHandler
import os

if __name__ == "__main__":
    handler_chain = LATimesScraperNewsHandler(ExcelSaverHandler())

    search_term = os.environ.get('SEARCH_TERM', '')
    filter = os.environ.get('FILTER', 'Newsletter')

    url = "https://www.latimes.com/"
    articles = []
    handler_chain.handle(articles, url, search_term, filter)
    
