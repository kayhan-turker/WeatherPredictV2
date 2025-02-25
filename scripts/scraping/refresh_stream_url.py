import yt_dlp
from scripts.utils import *

YOUTUBE_URL = "https://www.youtube.com/watch?v="


def get_stream_url(video_id):
    try:
        with yt_dlp.YoutubeDL({"format": "best", "quiet": True}) as ydl:
            return ydl.extract_info(f"{YOUTUBE_URL}{video_id}", download=False)["url"]
    except Exception as e:
        print_log("ERROR", f"Failed to fetch YouTube stream URL: {e}")
        return None
