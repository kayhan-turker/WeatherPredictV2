from core.metadata.video_source_metadata import *
from collections import Counter

video_metadata, _ = init_video_metadata_manager()
source_image_count = {}
image_count_max = 0

for source_id in video_metadata.keys():
    source_images_path = os.path.join(f"{FILTERED_IMAGES_PATH}{source_id}/")

    path_exists = os.path.exists(source_images_path)
    image_count = len(os.listdir(source_images_path)) if path_exists else 0
    source_image_count[source_id] = image_count

    if image_count > image_count_max:
        image_count_max = image_count

# Sort the dictionary
source_image_count = dict(sorted(source_image_count.items(), key=lambda item: item[1]))
# Get the mode
counter = Counter(source_image_count.values())
mode = [k for k, v in counter.items() if v == max(counter.values())]

for source_id, image_count in source_image_count.items():
    source_image_count[source_id] = round(image_count / mode[0], 3)

for k, v in source_image_count.items():
    print(f"{k:<5} | {v:<5}")
