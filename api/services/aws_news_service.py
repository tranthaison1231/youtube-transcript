import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_aws_news():
    """
    Scrape latest news from AWS Blog
    Returns a list of news articles with title, link, summary, and published_date
    """
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # Disable images, CSS, and fonts
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.managed_default_content_settings.stylesheets": 2,
            "profile.managed_default_content_settings.fonts": 2,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://aws.amazon.com/blogs/")
        # Wait for the main container to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".aws-directories-container")
            )
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        article_links = soup.find_all(
            "a", href=re.compile(r"https://aws.amazon.com/blogs/")
        )

        articles = []
        for article in article_links:
            link = article.get("href")
            print(link)

            if link:
                articles.append(
                    {
                        "title": "title",
                        "link": link,
                        "summary": "summary",
                        "published_date": "published_date",
                    }
                )

        return []

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
