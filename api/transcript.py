import json
from youtube_transcript_api import YouTubeTranscriptApi


def handler(request):
    video_id = request.get("query", {}).get("video_id")
    language = request.get("query", {}).get("language")
    if not video_id:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing video_id"})}
    try:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id, languages=[language]
            )
        except Exception:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return {"statusCode": 200, "body": json.dumps(transcript)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
