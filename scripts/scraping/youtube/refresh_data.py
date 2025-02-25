from scripts.scraping.request_log_manager import *
from scripts.localConfig import *

YOUTUBE_REQUEST_LOG_FIELDS = ["region", "latitude", "longitude", "crop_left", "crop_top", "crop_right", "crop_bottom"]

youtube_request_log_manager = LogManager(YOUTUBE_LOG_FILE, YOUTUBE_REQUEST_LOG_FIELDS, 0,
                                         {}, '<webcam_id>')

