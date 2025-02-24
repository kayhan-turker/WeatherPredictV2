import json
import re
from scripts.utils import *

WEBCAM_SCRAPE_LOG_FIELDS = ["last_updated_on", "crop_left", "crop_top", "crop_right", "crop_bottom"]
WEBCAM_SCRAPE_LOG_FIELD_DEFAULTS = {"last_updated_on": "2000-01-01T00:00:00.000Z"}  # Other field defaults 0 by default


def get_default_field_value(field):
    return 0 if field not in WEBCAM_SCRAPE_LOG_FIELD_DEFAULTS else WEBCAM_SCRAPE_LOG_FIELD_DEFAULTS[field]


def return_empty_field_dict():
    return {field: get_default_field_value(field) for field in WEBCAM_SCRAPE_LOG_FIELDS}


def return_empty_log_dict():
    return {'<webcam_id>': return_empty_field_dict()}


def read_webcam_scrape_log(file):
    try:
        with open(file, 'r') as f:
            content = f.read().strip()
            webcam_scrape_log = json.loads(content) if content else return_empty_log_dict()
    except (FileNotFoundError, json.JSONDecodeError):
        print_log("WARNING", "File not found, empty, or invalid. Creating empty JSON log.")
        webcam_scrape_log = return_empty_log_dict()

    for webcam_id, field_dict in webcam_scrape_log.items():
        # If webcam id has no fields listed
        if field_dict is None or not isinstance(field_dict, dict):
            print_log("WARNING", f"Webcam {webcam_id} missing field dictionary! Field dictionary added.")
            field_dict = return_empty_field_dict()

        for field in WEBCAM_SCRAPE_LOG_FIELDS:
            default_value = get_default_field_value(field)
            default_type = type(default_value)

            # If field is missing
            if field not in field_dict:
                print_log("WARNING", f"Webcam {webcam_id} missing field! Added field {field}.")
                value = default_value
            else:
                value = field_dict[field]
                value_type = type(value)

                # Check empty value for field
                if value is None or value == "" or value == "null":
                    value = default_value
                else:
                    # Otherwise is there a type mismatch?
                    if default_type is float or default_type is int:
                        value = re.sub(r'[^0-9.]]', '', value) if value_type is str else value
                        value = int(round(float(value))) if default_type is int else float(value)
                    elif default_type is str:
                        value = str(value)

            field_dict[field] = value
        webcam_scrape_log[webcam_id] = field_dict

    return webcam_scrape_log


def write_webcam_scrape_log(file, json_data):
    with open(file, 'w') as f:
        f.write('{\n' + ',\n'.join(
            f'    "{key}": {json.dumps(value, separators=(",", ":"))}'
            for key, value in json_data.items()
        ) + '\n}')