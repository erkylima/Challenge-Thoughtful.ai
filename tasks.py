from adapters.la_times_scraper_handler import LATimesScraperNewsHandler
from adapters.excel_saver_handler import ExcelSaverHandler
from robocorp.tasks import task
import os
import logging
logger = logging.getLogger(__name__)

@task
def newsletter_scraper():
    handler_chain = LATimesScraperNewsHandler(ExcelSaverHandler())
    logging.basicConfig(filename='output/extraction.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    search_term = os.environ.get('SEARCH_TERM', '')
    filters = os.environ.get('FILTER', 'Newsletter')
    months = int(os.environ.get('MONTHS', 0))

    url = "https://www.latimes.com/"
    articles = []
    handler_chain.handle(articles, url, search_term, filters, months)

if __name__ == "__main__":
    newsletter_scraper()
    
