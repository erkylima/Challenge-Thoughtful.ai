from adapters.la_times_scraper_handler import LATimesScraperNewsHandler
from adapters.excel_saver_handler import ExcelSaverHandler
import os
import logging
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    handler_chain = LATimesScraperNewsHandler(ExcelSaverHandler())
    logging.basicConfig(filename='output/extraction.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    search_term = os.environ.get('SEARCH_TERM', '')
    filter = os.environ.get('FILTER', 'Newsletter')

    url = "https://www.latimes.com/"
    articles = []
    handler_chain.handle(articles, url, search_term, filter)
    
