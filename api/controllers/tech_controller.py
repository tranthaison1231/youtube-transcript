from flask import Blueprint, jsonify
from concurrent.futures import ThreadPoolExecutor, as_completed
from api.services.bybygo_news_service import get_bybygo_news
from api.services.newsletter_news_service import get_newsletter_news
from api.services.remix_news_service import get_remix_news
from api.services.tanstack_news_service import get_tanstack_news
from api.services.tailwind_news_service import get_tailwind_news

tech_bp = Blueprint("tech", __name__, url_prefix="/tech")


@tech_bp.route("/news", methods=["GET"])
def get_tech_news_controller():
    with ThreadPoolExecutor(max_workers=2) as executor:
        bybygo_news = executor.submit(get_bybygo_news)
        newsletter_news = executor.submit(get_newsletter_news)
        tanstack_news = executor.submit(get_tanstack_news)
        remix_news = executor.submit(get_remix_news)
        tailwind_news = executor.submit(get_tailwind_news)

        news = []
        for future in as_completed(
            [bybygo_news, newsletter_news, tanstack_news, remix_news, tailwind_news]
        ):
            try:
                result = future.result()
                if result:
                    news.extend(result)
            except Exception as e:
                print(f"Error fetching news from one source: {e}")

    if news:
        sorted_news = sorted(news, key=lambda x: x["published_date"], reverse=True)
        filtered_30_news = sorted_news[:30]

        return jsonify(
            {
                "status": "success",
                "count": len(filtered_30_news),
                "news": filtered_30_news,
            }
        ), 200
    else:
        return jsonify({"status": "error", "message": "Failed to fetch news"}), 500
