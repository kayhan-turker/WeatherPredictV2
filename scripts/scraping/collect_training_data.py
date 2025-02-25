import time
from scripts.metadata.video_source_metadata import *
from scripts.scraping.labels.request_video_still import *
from scripts.scraping.labels.collect_labels import *


# Prepare logs

VIDEO_WIDTH = 960
VIDEO_HEIGHT = 540

stream_urls = {}
last_url_refresh = time.time()
stream_refresh_interval = 7200

last_data_refresh = 0
data_refresh_interval = 60

# Create directories
for youtube_id in video_source_metadata.keys():
    os.makedirs(STREAM_IMAGE_SAVE_PATH + youtube_id + '/', exist_ok=True)

# Refresh Loop
while True:
    # Wait enough time to do the next refresh
    if time.time() - last_data_refresh <= data_refresh_interval:
        time.sleep(0.5)
        continue
    last_data_refresh = time.time()
    print('=' * 200)

    # Check if stream url refresh is needed
    refresh_stream_urls = time.time() - last_url_refresh > stream_refresh_interval
    for youtube_id, log_field_dict in video_source_metadata.items():

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
        labels = collect_labels(dt_now, log_field_dict['region'], log_field_dict['latitude'],
                                log_field_dict['longitude'], log_field_dict['elevation'])
        label_output = f"{youtube_id};{datetime.strftime(dt_now, '%Y;%m;%d;%H;%M;%S')};{';'.join([str(label) for label in labels])}"
        with open(f"{LABEL_SAVE_PATH}{youtube_id}.txt", "a") as file:
            file.write(f"{label_output}\n")
        print_log("INFO", f"Saved label data: {label_output}")

    # Update refresh times if needed
    if refresh_stream_urls:
        last_url_refresh = time.time()
