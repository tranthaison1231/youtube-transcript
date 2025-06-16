from flask import Flask, request, jsonify
from youtube_transcript_api._api import YouTubeTranscriptApi

app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_transcript():
    video_id = request.args.get("video_id")
    language = request.args.get("language", "en")

    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400

    try:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id, languages=[language]
            )
        except Exception:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return jsonify(transcript), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
