from flask import Flask, jsonify, request
import requests


app = Flask(__name__)


@app.route("/youtube-transcript", methods=["GET"])
def get_transcript():
    video_id = request.args.get("video_id")

    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400

    try:
        transcript = requests.get(
            f"https://videoentity.com/videos/{video_id}/transcript"
        )
        return jsonify(transcript), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
