import requests


def fetch_and_process_transcript(video_id):
    url = f"https://videoentity.com/videos/{video_id}/transcript"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        scripts = ""
        for item in json_data.get("transcript", []):
            scripts += item.get("text", "")
        return scripts
    return None
