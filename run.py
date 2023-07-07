from scraper import WebsiteScraper
from data_saver import DataSaver
import os
from dotenv import load_dotenv


if __name__ == "__main__":
    # getting the env variables
    load_dotenv()
    url = str(os.getenv("INPUT_URL"))
    class_name = "quote"
    filename = str(os.getenv("OUTPUT_FILE"))
    proxy = str(os.getenv("PROXY"))

    # fetching & processing the data
    scraper = WebsiteScraper(url, class_name, proxy)
    quotes = scraper.scrape_website()

    # saving processed data into jsonl file
    saver = DataSaver(filename, quotes)
    saver.save_quotes_to_jsonl()

    # final console logging
    print(f"Quotes saved to {filename}")
