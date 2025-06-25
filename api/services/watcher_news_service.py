import requests
from bs4 import BeautifulSoup
import re

from api.utils.get_date_from_time_left import convert_to_iso


def get_watcher_news():
    """
    Scrape latest news from Watcher.Guru
    Returns a list of news articles with title, link, summary, and publishedDate
    """
    try:
        url = "https://watcher.guru/news/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        # Look for article links that contain "/community/en/articles/"
        article_links = soup.find_all("a", href=re.compile(r"/news/"))

        for link in article_links:
            link_url = link.get("href")
            title_el = link.parent.parent.find("h2", class_="cs-entry__title")
            time_el = link.parent.parent.find("div", class_="cs-meta-date")
            summary_el = link.parent.parent.find("div", class_="cs-entry__excerpt")

            title = title_el.contents[0].text.strip() if title_el else ""
            time = time_el.text.strip() if time_el else ""
            summary = summary_el.text.strip() if summary_el else ""

            published_date = convert_to_iso(time, "%b %d, %Y")

            article = {
                "title": title,
                "link": link_url,
                "summary": summary,
                "published_date": published_date,
            }
            if link_url and title and time:
                articles.append(article)

        return articles

    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
