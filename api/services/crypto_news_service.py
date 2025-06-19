import requests
from bs4 import BeautifulSoup
import time
import random

from api.utils.convert_timestamp_to_iso import convert_timestamp_to_iso


def get_crypto_news():
    """
    Scrape latest news from CoinMarketCap
    Returns a list of news articles with title, link, summary, and publishedDate
    """
    try:
        url = "https://cryptonews.com/news/bitcoin-news/"

        # Use realistic browser headers to avoid 403 errors
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }

        # Add a session for better cookie handling
        session = requests.Session()
        session.headers.update(headers)

        # Add a small delay to appear more human-like
        time.sleep(random.uniform(1, 3))

        response = session.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        # Look for article links that contain "/community/en/articles/"
        article_titles = soup.find_all(
            "h5", class_="archive-template-latest-news__title"
        )

        for article_title in article_titles:
            try:
                title = article_title.get_text(strip=True)
                summary_element = article_title.parent.find(
                    "div", class_="archive-template-latest-news__description"
                )
                summary = summary_element.get_text(strip=True)
                time_element = article_title.parent.find(
                    "div", class_="archive-template-latest-news__time"
                )

                time_left_text = time_element.get("data-utctime")

                time_iso = convert_timestamp_to_iso(time_left_text)

                link = article_title.parent.parent.get("href")

                if title and len(title) > 1 and time_iso:
                    article = {
                        "title": title,
                        "link": link,
                        "summary": summary,
                        "publishedDate": time_iso,
                    }
                    articles.append(article)
            except Exception as e:
                print(f"Error processing individual article: {e}")
                continue

        return articles

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
