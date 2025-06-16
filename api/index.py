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
        if transcript.status_code == 200:
            json_data = transcript.json()

            scripts = ""
            for item in json_data["transcript"]:
                scripts += item["text"]

            return jsonify({"scripts": scripts}, 200)
        else:
            return jsonify({"error": "Failed to get transcript"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
