import os
import requests
import re
from PIL import Image
from io import BytesIO
from datetime import datetime
from scripts.config import *

# ================================
#  CONSTANTS
# ================================

COMMON_DATETIME_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%Y/%m/%d %H:%M:%S",
    "%Y.%m.%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%S.%fZ",
    "%Y-%m-%d",
    "%d/%m/%Y %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
    "%H:%M:%S %Y-%m-%d",
    "%Y%m%d%H%M%S",
]


# ================================
#  READ WRITE FUNCTIONS
# ================================

def print_log(log_type, message):
    log_type = str.upper(log_type)
    log_color_code = LOG_COLORS[log_type] if log_type in LOG_COLORS else ""
    print(f"{log_color_code}[{str.upper(log_type)}] {datetime.now()}: {message}{LOG_COLORS['END']}")


def dict_to_json_list_string(field_vals):
    list_str = '{'
    for key, value in field_vals.items():
        list_str += '"' + key + '":"' + value + '",'
    return list_str[:-1] + '}'


def field_to_empty_json_list_string(fields):
    list_str = '{'
    for field in fields:
        list_str += '"' + field + '":null,'
    return list_str[:-1] + '}'


def get_url_page_text(url):
    response = requests.get(url)
    if response.status_code != 200:
        print_log("ERROR", f"Text extract failed! Url {url} not valid!")
        return None

    return response.text


def get_url_page_json(url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print_log("ERROR", f"Json extract failed! Url {url} not valid!")
        return None

    return response.json()


def search_in_text(text, search_pattern, group_num=1):
    match = re.search(search_pattern, text)
    if not match:
        print_log("ERROR", f"Search pattern {search_pattern} was not found!")
        return None

    return match.group(group_num)


# ================================
#  DATETIME FUNCTIONS
# ================================

def determine_datetime_format(datetime_str):
    for fmt in COMMON_DATETIME_FORMATS:
        try:
            datetime.strptime(datetime_str, fmt)
            return fmt
        except ValueError:
            continue
    return None


def convert_datetime_string(input_str, final_format):
    current_format = determine_datetime_format(input_str)
    if current_format is None:
        print_log("ERROR", f"Unable to parse the input datetime string: {input_str}")
        return input_str

    input_dt = datetime.strptime(input_str, current_format)
    return input_dt.strftime(final_format)


def string_date_is_greater_than(date_0, date_1, dt_format=None):
    dt_0 = datetime.strptime(date_0, dt_format if dt_format is not None else determine_datetime_format(date_0))
    dt_1 = datetime.strptime(date_1, dt_format if dt_format is not None else determine_datetime_format(date_1))
    return dt_0 > dt_1


def datetime_to_milliseconds(input_dt, dt_format=None):
    dt = datetime.strptime(input_dt, dt_format if dt_format is not None else determine_datetime_format(input_dt))
    return int(dt.timestamp() * 1000)


# ================================
#  IMAGE FUNCTIONS
# ================================

def save_url_image(image_url, file_path, file_name, show_current=False,
                   crop_left=0, crop_top=0, crop_right=0, crop_bottom=0):

    image_content = requests.get(image_url).content
    image = Image.open(BytesIO(image_content))

    if crop_right > crop_left and crop_bottom > crop_top:
        image = image.crop((crop_left, crop_top, crop_right, crop_bottom))

    if show_current:
        image.show()

    os.makedirs(file_path, exist_ok=True)
    image.save(f"{file_path}{file_name}.jpg")
    print_log("INFO", f"Image {file_name} saved in {file_path}.")

