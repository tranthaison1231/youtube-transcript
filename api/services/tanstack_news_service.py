from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re


def get_tanstack_news():
    """
    Scrape latest news from ByteByteGo RSS feed
    Returns a list of news articles with title, link, summary, and published_date
    """
    try:
        url = "https://tanstack.com/blog"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse RSS feed with BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        article_links = soup.find_all("a", href=re.compile(r"/blog/"))
        articles = []

        for link in article_links:
            title = link.contents[0].contents[0].text.strip()
            link_url = link.get("href")
            summary = link.contents[0].contents[2].text.strip()
            time = (
                link.contents[0]
                .contents[1]
                .contents[0]
                .text.strip()
                .split("on")[1]
                .strip()
            )

            published_date = ""
            try:
                # Parse the date string
                dt = datetime.strptime(time, "%b %d, %Y")
                # Convert to ISO format
                published_date = dt.isoformat()
            except Exception as e:
                published_date = ""

            if title and link_url and published_date:
                articles.append(
                    {
                        "title": title,
                        "link": "https://tanstack.com" + link_url,
                        "summary": summary,
                        "published_date": published_date,
                    }
                )

        return articles

    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
