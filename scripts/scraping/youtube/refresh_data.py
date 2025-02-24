from scripts.scraping.request_manager import *
from scripts.scraping.youtube.request_youtube_webcams import *
from scripts.scraping.request_sun_values import *
from scripts.localConfig import *

YOUTUBE_REQUEST_LOG_FIELDS = ["crop_left", "crop_top", "crop_right", "crop_bottom"]

windy_request_log_manager = RequestLogManager(YOUTUBE_LOG_FILE, YOUTUBE_REQUEST_LOG_FIELDS, 0,
                                              {}, '<webcam_id>')

