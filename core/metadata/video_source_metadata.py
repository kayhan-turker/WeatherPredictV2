from core.metadata.json_metadata_manager import *
from core.scrapers.request_location_data import *
from common.localConfig import *

# Quality: 0 = Blurry, 1 = Over Processed, 2 = Bad Exposure, 3 = Natural
# Static: 0 = Movement, 1 = Slight Shifts, 2 = Perfectly Static
VIDEO_METADATA_FIELDS = ["region", "latitude", "longitude", "elevation",
                                "crop_left", "crop_top", "crop_right", "crop_bottom",
                                "quality", "stillness"]
VIDEO_METADATA_DEFAULTS = {"region": "NA", "latitude": 0.0, "longitude": 0.0,
                                  "quality": 0, "stillness": 0}


def init_video_metadata_manager(validate_altitudes=False):
    video_metadata_manager = MetadataManager(SOURCE_STREAM_METADATA_FILE, VIDEO_METADATA_FIELDS, 0,
                                             VIDEO_METADATA_DEFAULTS, '<source_id>')
    video_metadata = video_metadata_manager.read_request_log()

    if validate_altitudes:
        print_log("INFO", "Validating location elevations.")
        for source_id, field_dict in video_metadata.items():
            latitude, longitude = field_dict['latitude'], field_dict['longitude']
            video_metadata[source_id]['elevation'] = request_location_data(latitude, longitude)['elevation']

        # Re-write json with updated metadata
        print_log("INFO", "Updating source metadata JSON file.")
        video_metadata_manager.write_request_log(video_metadata)

    return video_metadata, video_metadata_manager
