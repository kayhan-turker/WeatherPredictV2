from scripts.scraping.request_manager import *
from scripts.scraping.windy.request_windy_webcams import *
from scripts.scraping.request_sun_values import *
from scripts.localConfig import *

WINDY_REQUEST_LOG_FIELDS = ["last_updated_on", "crop_left", "crop_top", "crop_right", "crop_bottom"]
WINDY_REQUEST_LOG_DEFUALTS = {"last_updated_on": "2000-01-01T00:00:00.000Z"}  # Other field defaults 0 by default

windy_request_log_manager = RequestLogManager(WINDY_REQUEST_LOG_FIELDS, 0,
                                              WINDY_REQUEST_LOG_DEFUALTS, '<webcam_id>')

windy_webcam_log = windy_request_log_manager.read_request_log(WINDY_LOG_FILE)

for webcam_id in windy_webcam_log.keys():
    field_dict = windy_webcam_log[webcam_id]
    image_url, last_updated_on, latitude, longitude = request_webcam_data(webcam_id)
    if image_url is None:
        continue

    logged_date = field_dict["last_updated_on"]
    if string_date_is_greater_than(last_updated_on, logged_date):
        file_name = f"{last_updated_on[:10]}-{(last_updated_on[11:19]).replace(':', '-')}"
        file_path = f"{WINDY_IMAGE_SAVE_PATH}{webcam_id}/"
        save_url_image(image_url, file_path, file_name, False,
                       field_dict['crop_left'], field_dict['crop_top'],
                       field_dict['crop_right'], field_dict['crop_bottom'])
        windy_webcam_log[webcam_id]["last_updated_on"] = last_updated_on

    request_sun_data(latitude, longitude)

write_request_log(WINDY_LOG_FILE, windy_webcam_log)
