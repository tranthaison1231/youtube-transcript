from flask import Flask, jsonify, request
import requests
import yt_dlp


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


def get_latest_video_info(channel_url):
    ydl_opts = {
        "extract_flat": True,
        "playlistend": 1,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        if info is None or "entries" not in info:
            return None
        latest_video = info["entries"][0]
        return {
            "title": latest_video["title"],
            "url": latest_video["url"],
        }


@app.route("/youtube-latest-video", methods=["GET"])
def get_latest_video():
    channel_url = request.args.get("channel_url")
    if not channel_url:
        return jsonify({"error": "Missing channel_url"}), 400

    last_video = get_latest_video_info(channel_url)
    return jsonify({"last_video": last_video}, 200)
