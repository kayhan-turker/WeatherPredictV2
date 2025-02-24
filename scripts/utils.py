import os
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
from scripts.config import *


def print_log(log_type, message):
    log_type = str.upper(log_type)
    log_color_code = LOG_COLORS[log_type] if log_type in LOG_COLORS else ""
    print(f"{log_color_code}[{str.upper(log_type)}] {datetime.now()}: {message}{LOG_COLORS['END']}")


def string_date_is_greater_than(date_0, date_1):
    dt_0 = datetime.strptime(date_0, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt_1 = datetime.strptime(date_1, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt_0 > dt_1


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
