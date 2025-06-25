from flask import Flask
from api.controllers.youtube_controller import youtube_bp
from api.controllers.crypto_controller import crypto_bp
from api.controllers.tech_controller import tech_bp
from api.controllers.gold_controller import gold_bp

app = Flask(__name__)

app.register_blueprint(youtube_bp)
app.register_blueprint(crypto_bp)
app.register_blueprint(tech_bp)
app.register_blueprint(gold_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
