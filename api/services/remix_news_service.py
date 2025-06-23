import requests
from bs4 import BeautifulSoup

from api.utils.get_date_from_time_left import convert_to_iso
import re


def get_remix_news():
    """
    Scrape latest news from CoinMarketCap
    Returns a list of news articles with title, link, summary, and publishedDate
    """
    try:
        url = "https://remix.run/blog"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        # Look for article links that contain "/community/en/articles/"
        article_links = soup.find_all("a", href=re.compile(r"/blog/"))

        for article in article_links:
            link = article.get("href")
            title = (
                article.contents[2].text.strip() if len(article.contents) > 2 else ""
            )
            summary = (
                article.contents[3].text.strip() if len(article.contents) > 3 else ""
            )

            time = (
                article.contents[1].contents[0].text.strip()
                if len(article.contents) > 1
                else ""
            )

            if link and title and summary:
                articles.append(
                    {
                        "title": title,
                        "link": "https://remix.run" + link,
                        "summary": summary,
                        "published_date": convert_to_iso(time),
                    }
                )

        return articles

    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
