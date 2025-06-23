import requests
from bs4 import BeautifulSoup

from api.utils.get_date_from_time_left import convert_to_iso
import re


def get_tailwind_news():
    """
    Scrape latest news from CoinMarketCap
    Returns a list of news articles with title, link, summary, and publishedDate
    """
    try:
        url = "https://tailwindcss.com/blog"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        # Look for article links that contain "/community/en/articles/"
        article_links = soup.find_all("a", href=re.compile(r"/blog/"))

        for article_link in article_links:
            link = "https://tailwindcss.com" + article_link.get("href")
            time = article_link.parent.parent.parent.contents[0].text.strip()
            title = article_link.text.strip()
            summary = article_link.parent.contents[2].text.strip()

            published_date = convert_to_iso(time)

            is_exist_article = any(article["link"] == link for article in articles)

            if link and published_date and not is_exist_article and title and summary:
                articles.append(
                    {
                        "title": title,
                        "link": link,
                        "summary": summary,
                        "published_date": published_date,
                    }
                )

        return articles

    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
