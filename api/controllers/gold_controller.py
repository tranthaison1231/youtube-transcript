from flask import Blueprint, jsonify
from concurrent.futures import ThreadPoolExecutor, as_completed
from api.services.coincu_news_service import get_coincu_news
from api.services.coinmerketcap_news_service import get_coinmarketcap_news
from api.services.crypto_news_service import get_crypto_news

gold_bp = Blueprint("gold", __name__, url_prefix="/gold")


@gold_bp.route("/news", methods=["GET"])
def get_gold_news_controller():
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_coinmarketcap = executor.submit(get_coinmarketcap_news)
        future_coincu = executor.submit(get_coincu_news)
        future_crypto = executor.submit(get_crypto_news)

        news = []
        for future in as_completed(
            [future_coinmarketcap, future_coincu, future_crypto]
        ):
            try:
                result = future.result()
                if result:
                    news.extend(result)
            except Exception as e:
                print(f"Error fetching news from one source: {e}")

    if news:
        return jsonify({"status": "success", "count": len(news), "news": news}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to fetch news"}), 500
