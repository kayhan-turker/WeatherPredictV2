import time
from scripts.metadata.metadata_manager import *
from scripts.scraping.labels.request_video_still import *
from scripts.scraping.labels.collect_labels import *
from scripts.localConfig import *


# Prepare logs
YOUTUBE_REQUEST_LOG_FIELDS = ["region", "latitude", "longitude", "altitude",
                              "crop_left", "crop_top", "crop_right", "crop_bottom"]
YOUTUBE_REQUEST_LOG_DEFAULTS = {"region": "NA", "latitude": 0.0, "longitude": 0.0}
youtube_request_log_manager = LogManager(SOURCE_METADATA_FILE, YOUTUBE_REQUEST_LOG_FIELDS, 0,
                                         YOUTUBE_REQUEST_LOG_DEFAULTS, '<youtube_id>')
youtube_webcam_log = youtube_request_log_manager.read_request_log()
youtube_request_log_manager.write_request_log(youtube_webcam_log)

VIDEO_WIDTH = 960
VIDEO_HEIGHT = 540

stream_urls = {}
last_url_refresh = time.time()
stream_refresh_interval = 7200

last_data_refresh = 0
data_refresh_interval = 60

# Create directories
for youtube_id in youtube_webcam_log.keys():
    os.makedirs(STREAM_IMAGE_SAVE_PATH + youtube_id + '/', exist_ok=True)

# Refresh Loop
while True:
    # Wait enough time to do the next refresh
    if time.time() - last_data_refresh <= data_refresh_interval:
        time.sleep(0.5)
        continue
    last_data_refresh = time.time()

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
        file_path = f"{STREAM_IMAGE_SAVE_PATH}{youtube_id}/"
        file_name = f"{datetime.strftime(dt_now, '%Y-%m-%d-%H-%M-%S')}"

        result = save_video_screenshot(stream_urls[youtube_id], file_path, file_name, VIDEO_WIDTH, VIDEO_HEIGHT,
                                       log_field_dict["crop_left"], log_field_dict["crop_top"],
                                       log_field_dict["crop_right"], log_field_dict["crop_bottom"])
        if result == 0:
            stream_urls[youtube_id] = get_stream_url(youtube_id)
            continue

        # Save labels
        labels = collect_labels(dt_now, log_field_dict['region'], log_field_dict['latitude'], log_field_dict['longitude'])
        label_output = f"{youtube_id};{datetime.strftime(dt_now, '%Y;%m;%d;%H;%M;%S')};{';'.join([str(label) for label in labels])}"
        with open(f"{LABEL_SAVE_PATH}{youtube_id}.txt", "a") as file:
            file.write(f"{label_output}\n")
        print_log("INFO", f"Saved label data: {label_output}")

    # Update refresh times if needed
    if refresh_stream_urls:
        last_url_refresh = time.time()
