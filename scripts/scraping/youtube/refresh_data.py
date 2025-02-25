import time
import subprocess
from scripts.scraping.request_log_manager import *
from scripts.scraping.youtube.request_youtube_webcams import *
from scripts.scraping.labels.label_manager import *
from scripts.localConfig import *


# Prepare logs
YOUTUBE_REQUEST_LOG_FIELDS = ["region", "latitude", "longitude", "crop_left", "crop_top", "crop_right", "crop_bottom"]
YOUTUBE_REQUEST_LOG_DEFAULTS = {"region": "NA", "latitude": 0.0, "longitude": 0.0}
youtube_request_log_manager = LogManager(YOUTUBE_LOG_FILE, YOUTUBE_REQUEST_LOG_FIELDS, 0,
                                         YOUTUBE_REQUEST_LOG_DEFAULTS, '<youtube_id>')
youtube_webcam_log = youtube_request_log_manager.read_request_log()

stream_urls = {}
last_url_refresh = time.time()
stream_refresh_interval = 7200

last_data_refresh = 0
data_refresh_interval = 10

# Create directories
for youtube_id in youtube_webcam_log.keys():
    os.makedirs(YOUTUBE_IMAGE_SAVE_PATH + youtube_id + '/', exist_ok=True)

# Refresh Loop
while True:
    # Wait enough time to do the next refresh
    if time.time() - last_data_refresh <= data_refresh_interval:
        time.sleep(0.5)
        continue

    # Check if stream url refresh is needed
    refresh_stream_urls = time.time() - last_url_refresh > stream_refresh_interval
    for youtube_id, log_field_dict in youtube_webcam_log.items():

        # Get stream urls if needed
        if refresh_stream_urls or youtube_id not in stream_urls:
            print_log("INFO", f"Refreshing YouTube stream URL for video id {youtube_id}.")
            stream_urls[youtube_id] = get_stream_url(youtube_id)

        # If stream url did not update, continue
        if not stream_urls[youtube_id]:
            print_log("ERROR", f"Stream url for video id {youtube_id} not retrieved.")
            continue

        # Get file name and path
        dt_now = datetime.now()
        file_name = f"{datetime.strftime(dt_now, '%Y-%m-%d-%H-%M-%S')}"
        file_path = f"{YOUTUBE_IMAGE_SAVE_PATH}{youtube_id}/"
        output_image = f"{file_path + file_name}.jpg"

        # Get screenshot of video
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", stream_urls[youtube_id], "-frames:v", "1", "-vf", "scale=960:-1", "-q:v", "1", output_image],
            capture_output=True, text=True)

        # If failed, refresh stream url and continue
        if result.returncode != 0:
            print_log("ERROR", f"Video screenshot failed: {result.stderr}. Refreshing stream url for {youtube_id}")
            stream_urls[youtube_id] = get_stream_url(youtube_id)
            continue

        # Save labels
        labels = get_labels(dt_now, log_field_dict['region'], log_field_dict['latitude'], log_field_dict['longitude'])
        label_output = f"{youtube_id};{datetime.strftime(dt_now, '%Y;%m;%d;%H;%M;%S')};{';'.join([str(label) for label in labels])}"
        with open(LABEL_DATA_FILE, "a") as file:
            file.write(f"{label_output}\n")
        print_log("INFO", f"Saved label data: {label_output}")

    # Update refresh times if needed
    last_data_refresh = time.time()
    if refresh_stream_urls:
        last_url_refresh = time.time()
