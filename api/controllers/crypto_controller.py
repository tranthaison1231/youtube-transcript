from flask import Blueprint, jsonify
from concurrent.futures import ThreadPoolExecutor, as_completed
from api.services.coincu_news_service import get_coincu_news
from api.services.coinmerketcap_news_service import get_coinmarketcap_news
from api.services.crypto_news_service import get_crypto_news
from api.services.watcher_news_service import get_watcher_news

crypto_bp = Blueprint("crypto", __name__, url_prefix="/crypto")


@crypto_bp.route("/news", methods=["GET"])
def get_crypto_news_controller():
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_coinmarketcap = executor.submit(get_coinmarketcap_news)
        future_coincu = executor.submit(get_coincu_news)
        future_crypto = executor.submit(get_crypto_news)
        future_watcher = executor.submit(get_watcher_news)

        news = []
        for future in as_completed(
            [future_coinmarketcap, future_coincu, future_crypto, future_watcher]
        ):
            try:
                result = future.result()
                if result:
                    news.extend(result)
            except Exception as e:
                print(f"Error fetching news from one source: {e}")

    if news:
        sorted_news = sorted(news, key=lambda x: x["published_date"], reverse=True)

        return jsonify(
            {
                "status": "success",
                "count": len(sorted_news),
                "news": sorted_news,
            }
        ), 200
    else:
        return jsonify({"status": "error", "message": "Failed to fetch news"}), 500
