import yt_dlp, subprocess
from scripts.utils import *

YOUTUBE_URL = "https://www.youtube.com/watch?v="


def get_stream_url(video_id):
    try:
        with yt_dlp.YoutubeDL({"format": "best", "quiet": True}) as ydl:
            return ydl.extract_info(f"{YOUTUBE_URL}{video_id}", download=False)["url"]
    except Exception as e:
        print_log("ERROR", f"Failed to fetch YouTube stream URL: {e}")
        return None


def save_video_screenshot(stream_url, file_path, file_name, width, height, crop_left, crop_top, crop_right, crop_bottom):
    output_image = f"{file_path}{file_name}.jpg"

    # Get screenshot of video
    transform_str = (f"scale={width}:-1,crop={width - crop_left - crop_right}:"
                     f"{height - crop_top - crop_bottom}:x={crop_left}:y={crop_top}")

    result = subprocess.run(
        ["ffmpeg", "-y", "-i", stream_url, "-frames:v", "1", "-vf",
         transform_str, "-q:v", "1", output_image], capture_output=True, text=True)

    # If failed, refresh stream url and continue
    if result.returncode != 0:
        print_log("ERROR", f"Video screenshot failed: {result.stderr}")
        return 0
    return 1
