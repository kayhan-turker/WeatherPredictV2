from scripts.scraping.request_log_manager import *
from scripts.scraping.windy.request_windy_webcam import *
from scripts.scraping.labels.request_sun_values import *
from scripts.localConfig import *

WINDY_REQUEST_LOG_FIELDS = ["last_updated_on", "crop_left", "crop_top", "crop_right", "crop_bottom"]
WINDY_REQUEST_LOG_DEFAULTS = {"last_updated_on": "2000-01-01T00:00:00.000Z"}  # Other field defaults 0 by default

windy_request_log_manager = LogManager(WINDY_LOG_FILE, WINDY_REQUEST_LOG_FIELDS, 0,
                                       WINDY_REQUEST_LOG_DEFAULTS, '<webcam_id>')

windy_webcam_log = windy_request_log_manager.read_request_log()

for webcam_id in windy_webcam_log.keys():
    field_dict = windy_webcam_log[webcam_id]
    image_url, last_updated_on, latitude, longitude = request_webcam_data(webcam_id)
    if image_url is None:
        continue

    logged_date = field_dict["last_updated_on"]
    if string_date_is_greater_than(last_updated_on, logged_date, "%Y-%m-%dT%H:%M:%S.%fZ"):
        file_name = f"{last_updated_on[:10]}-{(last_updated_on[11:19]).replace(':', '-')}"
        file_path = f"{WINDY_IMAGE_SAVE_PATH}{webcam_id}/"
        save_url_image(image_url, file_path, file_name, False,
                       field_dict['crop_left'], field_dict['crop_top'],
                       field_dict['crop_right'], field_dict['crop_bottom'])
        windy_webcam_log[webcam_id]["last_updated_on"] = last_updated_on

        request_sun_values(latitude, longitude)

windy_request_log_manager.write_request_log(windy_webcam_log)
