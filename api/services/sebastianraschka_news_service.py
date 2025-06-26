import requests
from bs4 import BeautifulSoup
from email.utils import parsedate_to_datetime


def get_sebastianraschka_news():
    """
    Scrape latest news from ByteByteGo RSS feed
    Returns a list of news articles with title, link, summary, and published_date
    """
    try:
        url = "https://magazine.sebastianraschka.com/feed"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse RSS feed with BeautifulSoup
        soup = BeautifulSoup(response.content, "xml")
        articles = []

        # Find all items in the RSS feed
        items = soup.find_all("item")

        for item in items[:10]:  # Get latest 10 articles
            try:
                # Extract title from CDATA
                title_elem = item.find("title")
                title = title_elem.text.strip() if title_elem else ""

                # Extract link
                link_elem = item.find("link")
                link = link_elem.text.strip() if link_elem else ""

                # Extract description/summary from CDATA
                description_elem = item.find("description")
                summary = ""
                if description_elem:
                    # Parse HTML content from description
                    desc_soup = BeautifulSoup(description_elem.text, "html.parser")
                    # Get text content, remove extra whitespace
                    summary_text = desc_soup.get_text(separator=" ", strip=True)
                    # Limit to 300 characters
                    summary = (
                        summary_text[:300] + "..."
                        if len(summary_text) > 300
                        else summary_text
                    )

                # Extract and parse publication date
                pubdate_elem = item.find("pubDate")
                published_date = ""
                if pubdate_elem:
                    try:
                        # Parse RSS date format (e.g., "Thu, 19 Jun 2025 15:30:36 GMT")
                        dt = parsedate_to_datetime(pubdate_elem.text)
                        # Convert to ISO format
                        published_date = dt.isoformat()
                    except Exception as e:
                        published_date = ""
                else:
                    published_date = ""

                # Only add article if we have at least title and link
                if title and link and published_date:
                    article = {
                        "title": title,
                        "link": link,
                        "summary": summary,
                        "published_date": published_date,
                    }
                    articles.append(article)

            except Exception as e:
                print(f"Error processing item: {e}")
                continue

        return articles

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
