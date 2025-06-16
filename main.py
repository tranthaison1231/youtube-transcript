from youtube_transcript_api._api import YouTubeTranscriptApi


transcript = YouTubeTranscriptApi.get_transcript("P4GLeHsGXpc", languages=["vi"])

print(transcript)
