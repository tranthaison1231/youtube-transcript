from flask import Flask, jsonify
from youtube_transcript_api._api import YouTubeTranscriptApi


app = Flask(__name__)


@app.route("/youtube-transcript", methods=["GET"])
def get_transcript():
    # video_id = request.args.get("video_id")
    # language = request.args.get("language", "en")

    # if not video_id:
    #     return jsonify({"error": "Missing video_id"}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            "P4GLeHsGXpc", languages=["vi"]
        )
        return jsonify(transcript), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
