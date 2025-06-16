from flask import Flask, jsonify
from youtube_transcript_api._api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig


app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_transcript():
    # video_id = request.args.get("video_id")
    # language = request.args.get("language", "en")

    # if not video_id:
    #     return jsonify({"error": "Missing video_id"}), 400

    try:
        ytt_api = YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
                proxy_username="vpxyvgfb",
                proxy_password="4jpqjemzqrlr",
            )
        )
        transcript = ytt_api.get_transcript("P4GLeHsGXpc", languages=["vi"])
        return jsonify(transcript), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
