import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_real_python_news():
    """
    Scrape latest news from Real Python using RSS feed (since main site uses JavaScript)
    Returns a list of news articles with title, link, summary, and published_date
    """
    try:
        # Real Python has an RSS feed that doesn't require JavaScript
        url = "https://realpython.com/atom.xml"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse RSS/Atom feed
        soup = BeautifulSoup(response.content, "xml")
        articles = []

        # Find all entries in the Atom feed
        entries = soup.find_all("entry")

        for entry in entries:
            title_elem = entry.find("title")
            title = title_elem.text.strip() if title_elem else ""

            link_elem = entry.find("link")
            link_url = link_elem.get("href") if link_elem else ""

            summary_elem = entry.find("summary") or entry.find("content")
            summary = ""
            if summary_elem:
                summary_soup = BeautifulSoup(summary_elem.text, "html.parser")
                summary = summary_soup.get_text(separator=" ", strip=True)[:300]

            updated_elem = entry.find("updated")
            published_date = updated_elem.text if updated_elem else ""

            forbidden_keywords = ["podcast", "course", "video", "quiz", "conference"]
            title_lower = title.lower()
            summary_lower = summary.lower()

            is_article = (
                all(keyword not in title_lower for keyword in forbidden_keywords)
                and all(keyword not in summary_lower for keyword in forbidden_keywords)
                and len(summary) > 30
            )

            if is_article and title and link_url and published_date:
                articles.append(
                    {
                        "title": title,
                        "link": link_url,
                        "summary": summary,
                        "published_date": published_date,
                    }
                )

        return articles

    except Exception as e:
        print(f"RSS feed failed, trying alternative method: {e}")
        return []
