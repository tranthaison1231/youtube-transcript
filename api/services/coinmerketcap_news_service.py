from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re


def get_coinmarketcap_news():
    """
    Scrape latest news from CoinMarketCap
    Returns a list of news articles with title, link, summary, and publishedDate
    """
    try:
        url = "https://coinmarketcap.com/headlines/news/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        # Look for article links that contain "/community/en/articles/"
        article_links = soup.find_all("a", href=re.compile(r"/community/en/articles/"))

        for link in article_links:
            article_container = link.parent.parent.parent
            title = link.text.strip()
            link_url = link.get("href")
            published_date = datetime.now().isoformat()
            summary = article_container.contents[1].contents[1].text.strip()

            article = {
                "title": title,
                "link": link_url,
                "summary": summary,
                "published_date": published_date,
            }
            if article["title"] and article["title"] not in [
                a["title"] for a in articles
            ]:
                articles.append(article)

        return articles

    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
