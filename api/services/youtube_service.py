import yt_dlp


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
            "video_id": latest_video["id"],
        }
