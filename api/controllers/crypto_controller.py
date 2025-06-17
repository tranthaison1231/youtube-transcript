from flask import Blueprint, jsonify, request

crypto_bp = Blueprint("crypto", __name__)


@crypto_bp.route("/news", methods=["GET"])
def get_crypto_price():
    # Placeholder logic; replace with real API call or service
    symbol = request.args.get("symbol", "BTC")
    price = 50000  # Example static price
    return jsonify({"symbol": symbol, "price": price})
