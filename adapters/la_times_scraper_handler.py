import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from adapters.errors import ExtractionError
import os
from adapters.base_handler import BaseHandler, NewsArticle
import time


class LATimesScraperNewsHandler(BaseHandler):
    def __init__(self, next_handler=None):
        super().__init__(next_handler)
        # Configurações para o modo headless
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  
        
    def handle(self, articles: list[NewsArticle], url: str, search_phrase: str, filter: str):
        self.browser.get(url)

        try: 
            self._perform_search(search_phrase)
            self._set_filter(filter)
            self.attempt_again(self._select_lastest, 5)
            self.attempt_again(self._scrape_news, 5, articles, search_phrase)
        except Exception as e:
            print(f"Error occurred: {e}")
        finally: 
            self.browser.quit()               
        
        if self.next_handler:
            articles.extend(super().handle(articles, \
                                            url, search_phrase, filter))
        return articles
    
    def _perform_search(self, phrase):
        try:
            search_button = self.browser.find_element(By.CSS_SELECTOR, \
                                                    'button[data-element="search-button"]')        
            search_button.click()
            search_box = self.browser.find_element(By.NAME,"q")
            search_box.send_keys(phrase + Keys.ENTER)
        except Exception as e:
            raise RuntimeError(ExtractionError.PERFORM_SEARCH_NEWSLETTER_ERROR) from e
        
    def _set_filter(self, filter):
        try:
            filter_button = self.browser.find_element(By.CSS_SELECTOR, \
                                                    'button[class="button filters-open-button"]')        
            filter_button.click()
            filter_menu = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.search-filter-menu[data-name="Type"]'))
            )
            see_all_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "search-filter")][.//p[text()="Type"]]//button[contains(@class, "see-all-button")]'))
            )
            see_all_button.click()        
            
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//ul[contains(@class, "search-filter-menu")][@data-name="Type"]//li'))
            )
            # Encontre todos os elementos li dentro do ul
            filter_items = filter_menu.find_elements(By.TAG_NAME, 'li')

            for item in filter_items:
                span = item.find_element(By.TAG_NAME, 'span')
                if span.text == filter:
                    checkbox = item.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')
                    checkbox.click()
                    break
            apply_button = self.browser.find_element(By.CSS_SELECTOR, \
                                                    'button[class="button apply-button"]')        
            apply_button.click()
        except Exception as e:
            raise RuntimeError(ExtractionError.FILTER_SELECTION_ERROR) from e

    def _select_lastest(self):
        try:
            select_element = WebDriverWait(self.browser, 5000).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'select.select-input[name="s"]'))
            )
            
            self.browser.execute_script("arguments[0].scrollIntoView(true);", select_element)

            WebDriverWait(self.browser, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'select.select-input[name="s"]'))
            )
            select = Select(select_element)
            select.select_by_value('1')

        except Exception as e:
            print(e)
            ExtractionError.SELECT_LATEST_ERROR
    
    def _scrape_news(self, articles: list[NewsArticle], search_phrase):        
        results_is_visible = EC.presence_of_element_located(
                                            (By.CLASS_NAME, "search-results-module-results-menu"))
        results_container = WebDriverWait(self.browser, 10).until(results_is_visible)    

        list_items = results_container.find_elements(By.TAG_NAME, "li")
        for li in list_items:
            try:

                promo_element = li.find_element(By.CSS_SELECTOR, \
                                                'ps-promo.promo-position-large.promo-medium')
                
                title = promo_element.find_element(By.CSS_SELECTOR, \
                                                'h3.promo-title a').text                
                description = ""
                try:
                    description = promo_element.find_element(By.CSS_SELECTOR, \
                                                            'p.promo-description').text
                except Exception as e:
                    print(ExtractionError.GETTING_DESCRIPTION_ERROR)
                
                date = promo_element.find_element(By.CSS_SELECTOR, \
                                                'p.promo-timestamp').text
                image_filename = ""
                try:
                    image_element = promo_element.find_element(By.CSS_SELECTOR, \
                                                            'div.promo-media picture img')
                    
                    image_src = image_element.get_attribute('src')
                    image_filename = image_src.split('/')[-1]  # Pega o último segmento da URL
                    self._download_image(image_src, image_filename)
                except Exception as e:
                    print(ExtractionError.GETTING_IMAGE_ERROR)
                article = NewsArticle(title, date, description, image_filename)
                article.analyze_content(search_phrase)
                articles.append(article)                       
            except Exception as e:
                print(e)
                raise RuntimeError(ExtractionError.APPENDING_NEWSLETTER_ERROR) from e    


    def _download_image(self, url, file_path):
        response = requests.get(url)
        
        if response.status_code == 200:
            path = "output/images"
            
            if not os.path.exists(path):
                os.makedirs(path)
            
            file_name = os.path.join(path, os.path.basename(file_path))
            
            with open(file_name, 'wb') as file:
                file.write(response.content)
            
            return file_name
        else:
            raise FileNotFoundError(f"Failed to download image. Status code: {response.status_code}")
