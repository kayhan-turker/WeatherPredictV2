import time
from core.metadata.video_source_metadata import *
from core.scrapers.request_video_still import *
from core.scrapers.collect_labels import *
from common.config import *


# Prepare logs

VIDEO_WIDTH = 960
VIDEO_HEIGHT = 540

stream_urls = {}
last_url_refresh = time.time()
stream_refresh_interval = 7200

last_data_refresh = 0
data_refresh_interval = 60

video_metadata, _ = init_video_metadata_manager(validate_altitudes=VALIDATE_ALTITUDES_BEFORE_DATA_COLLECTION)

# Create directories
for source_id in video_metadata.keys():
    os.makedirs(STREAM_IMAGE_SAVE_PATH + source_id + '/', exist_ok=True)

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
    for source_id, log_field_dict in video_metadata.items():

        # Get stream urls if needed
        if refresh_stream_urls or source_id not in stream_urls:
            print_log("INFO", f"Refreshing source stream URL for video id {source_id}.")
            stream_urls[source_id] = get_stream_url(source_id)

        # If stream url did not update, continue
        if not stream_urls[source_id]:
            print_log("ERROR", f"Stream url for video id {source_id} not retrieved.")
            continue

        # Get file name and path
        dt_now = datetime.now()
        file_path = f"{STREAM_IMAGE_SAVE_PATH}{source_id}/"
        file_name = f"{datetime.strftime(dt_now, '%Y-%m-%d-%H-%M-%S')}"

        result = save_video_screenshot(stream_urls[source_id], file_path, file_name, VIDEO_WIDTH, VIDEO_HEIGHT,
                                       log_field_dict["crop_left"], log_field_dict["crop_top"],
                                       log_field_dict["crop_right"], log_field_dict["crop_bottom"])
        if result == 0:
            stream_urls[source_id] = get_stream_url(source_id)
            continue

        # Save labels
        label = collect_labels(dt_now, log_field_dict['region'], log_field_dict['latitude'],
                                log_field_dict['longitude'], log_field_dict['elevation'])
        write_label_to_file(source_id, dt_now, label)

    # Update refresh times if needed
    if refresh_stream_urls:
        last_url_refresh = time.time()
