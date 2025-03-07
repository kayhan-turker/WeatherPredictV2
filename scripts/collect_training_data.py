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

source_metadata, _ = init_video_metadata_manager(validate_altitudes=VALIDATE_ALTITUDES_BEFORE_DATA_COLLECTION)

# Create directories

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
    for source_id, source_id_metadata in source_metadata.items():

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

        # Get labels
        label = collect_labels(dt_now, source_id_metadata['region'], source_id_metadata['latitude'],
                               source_id_metadata['longitude'], source_id_metadata['elevation'])

        # Skip if needed (any None types, day only source at night)
        if (any(x is None or x == 'None' for x in label) or
                (source_id_metadata['only_day'] and label[LABEL_INDEX_SUN_ALTITUDE] < 0)):
            print_log("WARNING", f"Skipped data entry for {source_id}.")
            continue

        # Save screenshot
        file_path = f"{UNFILTERED_IMAGES_PATH}{source_id}/"
        file_name = f"{datetime.strftime(dt_now, '%Y-%m-%d-%H-%M-%S')}"
        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)

        result = save_video_screenshot(stream_urls[source_id], file_path, file_name, VIDEO_WIDTH, VIDEO_HEIGHT,
                                       source_id_metadata["crop_left"], source_id_metadata["crop_top"],
                                       source_id_metadata["crop_right"], source_id_metadata["crop_bottom"])

        # If screenshot failed, do not save label, attempt refresh stream
        if result == 0:
            stream_urls[source_id] = get_stream_url(source_id)
            continue

        # Save labels
        write_label_to_file(source_id, dt_now, label)

    # Update refresh times if needed
    if refresh_stream_urls:
        last_url_refresh = time.time()
