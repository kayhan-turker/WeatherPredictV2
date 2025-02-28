from scripts.metadata.json_metadata_manager import *
from scripts.scraping.labels.request_location_data import *
from scripts.localConfig import *

# Quality: 0 = Blurry, 1 = Over Processed, 2 = Bad Exposure, 3 = Natural
# Static: 0 = Movement, 1 = Slight Shifts, 2 = Perfectly Static
VIDEO_SOURCE_METADATA_FIELDS = ["region", "latitude", "longitude", "elevation",
                                "crop_left", "crop_top", "crop_right", "crop_bottom",
                                "quality", "static"]
VIDEO_SOURCE_METADATA_DEFAULTS = {"region": "NA", "latitude": 0.0, "longitude": 0.0,
                                  "quality": 0, "static": 0}

video_source_metadata_manager = MetadataManager(SOURCE_METADATA_FILE, VIDEO_SOURCE_METADATA_FIELDS, 0,
                                                VIDEO_SOURCE_METADATA_DEFAULTS, '<youtube_id>')
video_source_metadata = video_source_metadata_manager.read_request_log()

# Print validate altitudes
print_log("INFO", "Validating location elevations.")
for source_id, field_dict in video_source_metadata.items():
    latitude, longitude = field_dict['latitude'], field_dict['longitude']
    video_source_metadata[source_id]['elevation'] = request_location_data(latitude, longitude)['elevation']

# Re-write json with updated metadata
print_log("INFO", "Updating source metadata JSON file.")
video_source_metadata_manager.write_request_log(video_source_metadata)
