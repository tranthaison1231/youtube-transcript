import requests
from bs4 import BeautifulSoup

from api.utils.get_date_from_time_left import get_date_from_time_left


def get_coincu_news():
    """
    Scrape latest news from CoinMarketCap
    Returns a list of news articles with title, link, summary, and publishedDate
    """
    try:
        url = "https://coincu.com/news/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        articles = []

        # Look for article links that contain "/community/en/articles/"
        article_links = soup.find_all("div", class_="post-item")

        for article in article_links:
            title_part = article.find("h5", class_="post-title")
            title = title_part.find("a").text.strip()
            link = title_part.find("a")["href"]
            summary_element = article.find("p", class_="from_the_blog_excerpt")
            summary = (
                summary_element.text.strip()
                if summary_element and summary_element.text
                else ""
            )

            time_left = article.find("div", class_="minusposts").contents[0]
            time_left_text = time_left.text.strip()

            if title and link and summary:
                articles.append(
                    {
                        "title": title,
                        "link": link,
                        "summary": summary,
                        "published_date": get_date_from_time_left(time_left_text),
                    }
                )

        return articles

    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
