import torchvision.transforms as transforms
import numpy as np
import requests
import os
import re
from datetime import datetime
from io import BytesIO
from PIL import Image
from scripts.constants import *

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
    "%Y-%m-%d-%H-%M-%S",
    "%Y;%m;%d;%H;%M;%S",
]


# ================================
#  READ WRITE FUNCTIONS
# ================================

def print_log(log_type, message):
    log_type = str.upper(log_type)
    log_color_code = LOG_COLORS[log_type] if log_type in LOG_COLORS else ""
    print(f"{log_color_code}[{str.upper(log_type)}] {datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')}: {message}{LOG_COLORS['END']}")


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
        print_log("WARNING", f"Search pattern {search_pattern} was not found!")
        return None

    return match.group(group_num) if match and group_num <= match.lastindex else None


def count_text_lines_in_directory(directory):
    record_count = 0
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                record_count += np.count_nonzero([bool(line.strip()) for line in file])
    return record_count


def get_text_file_list_in_directory(directory):
    file_list = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_list.append(filename.split('.')[0])
    return file_list


# ================================
#  DATETIME FUNCTIONS
# ================================

def get_datetime_format(in_str):
    for fmt in COMMON_DATETIME_FORMATS:
        try:
            datetime.strptime(in_str, fmt)
            return fmt
        except ValueError:
            continue
    return None


def convert_datetime_string(in_str, final_format):
    current_format = get_datetime_format(in_str)
    if current_format is None:
        print_log("ERROR", f"Unable to parse the input datetime string: {in_str}")
        return in_str

    input_dt = datetime.strptime(in_str, current_format)
    return input_dt.strftime(final_format)


def string_date_is_greater_than(date_str_0, date_str_1, dt_format=None):
    dt_0 = datetime.strptime(date_str_0, dt_format if dt_format is not None else get_datetime_format(date_str_0))
    dt_1 = datetime.strptime(date_str_1, dt_format if dt_format is not None else get_datetime_format(date_str_1))
    return dt_0 > dt_1


def datetime_to_milliseconds(in_dt, dt_format=None):
    dt = datetime.strptime(in_dt, dt_format if dt_format is not None else get_datetime_format(in_dt))
    return int(dt.timestamp() * 1000)


def get_decimal_year(in_dt):
    year_start = datetime(in_dt.year, 1, 1)
    year_end = datetime(in_dt.year + 1, 1, 1)
    return in_dt.year + (in_dt - year_start).total_seconds() / (year_end - year_start).total_seconds()


def get_decimal_day(dt):
    return (dt.hour + (dt.minute + dt.second / 60) / 60) / 24


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


def show_tensor_image(tensor):
    print(tensor.ndim)
    if tensor.ndim == 4:  # If a batch, take the first image
        tensor = tensor[0]

    to_pil = transforms.ToPILImage()
    image = to_pil(tensor.cpu().detach())
    image.show()
