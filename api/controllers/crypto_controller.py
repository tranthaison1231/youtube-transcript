from flask import Blueprint, jsonify
from api.services.crypto_news_service import get_coinmarketcap_news

crypto_bp = Blueprint("crypto", __name__, url_prefix="/crypto")


@crypto_bp.route("/news", methods=["GET"])
def get_crypto_news():
    # Get news from Cointelegraph
    news = get_coinmarketcap_news()

    if news:
        return jsonify({"status": "success", "count": len(news), "news": news}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to fetch news"}), 500
