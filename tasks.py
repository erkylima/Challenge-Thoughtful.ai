from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem

browser = Selenium()

def store_web_page_content():
    browser.open_browser(url="https://robotframework.org")
    text = browser.get_text("css:body")
    file_system = FileSystem()
    file_system.create_file("output/web_page_content.txt", text, overwrite=True)
    browser.screenshot("css:h1", "output/screenshot.png")

def minimal_task():
    try:
        store_web_page_content()
    finally:
        browser.close_browser()
    



if __name__ == "__main__":
    minimal_task()