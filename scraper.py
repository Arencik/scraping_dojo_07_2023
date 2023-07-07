from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


class WebsiteScraper:
    def __init__(self, url, class_name, proxy):
        self.url = url
        self.class_name = class_name
        self.proxy = proxy

    # main scrapping function
    def scrape_website(self):
        driver = self.setup_driver()

        # nested function used to scrap the website
        def scrapper():
            try:
                quotes = []  # initializing the final output list
                next_button_present = (
                    True  # bool determining if program should continue to the next page
                )
                page_index = 1  # page index

                print("Quoting on page: " + str(page_index))

                while next_button_present:
                    page_url = f"{self.url}/page/{page_index}"  # accessing pages by page number
                    driver.get(page_url)

                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CLASS_NAME, self.class_name))
                    )  # waiting for quotes to render
                    quote_elements = driver.find_elements(
                        By.CLASS_NAME, self.class_name
                    )

                    # fetched data processing
                    for quote_element in quote_elements:
                        quote = self.extract_quote_data(quote_element)
                        quotes.append(quote)
                    # progress log printing statement
                    print(
                        "Data from page number "
                        + str(page_index)
                        + " extracted successfully"
                    )
                    next_button_present = self.is_next_button_present(driver)
                    page_index += 1

                return quotes
            finally:
                driver.quit()

        try:  # try-except to handle proxy timeout
            print("Trying with proxy")
            return scrapper()
        except:
            print("Connection timeout")
            print("Trying without proxy")
            driver = self.setup_driver(is_proxy=False)
            return scrapper()

    # driver setup function
    def setup_driver(self, is_proxy=True):
        service = Service(ChromeDriverManager().install())
        options = Options()
        options.add_argument("--headless")

        # Configure proxy settings
        if is_proxy:
            options.add_argument(f"--proxy-server={self.proxy}")

        driver = webdriver.Chrome(service=service, options=options)
        return driver

    # data processing function
    def extract_quote_data(self, quote_element):
        text_element = quote_element.find_element(By.CLASS_NAME, "text")
        author_element = quote_element.find_element(By.CLASS_NAME, "author")
        tags_elements = quote_element.find_elements(By.CLASS_NAME, "tags")

        text = text_element.text[1:-1]
        author = author_element.text
        tags = tags_elements[0].text[6:].split(" ")
        quote = {"text": text, "by": author, "tags": tags}
        return quote

    # "next" element checking function
    def is_next_button_present(self, driver):
        try:
            driver.find_element(By.CLASS_NAME, "next")
            return True
        except NoSuchElementException:
            return False
