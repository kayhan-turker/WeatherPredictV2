from core.metadata.label_source_metadata import *


def request_web_labels(region, latitude, longitude):
    validate_label_source_metadata()

    website = REGION_WEBSITES[region]
    url = WEBSITE_URLS[website].replace(LATITUDE_PLACEHOLDER, str(latitude)).replace(LONGITUDE_PLACEHOLDER, str(longitude))
    url_page_text = re.sub(r"\s+", " ", get_url_page_text(url))

    label = {}
    for label_name in WEB_LABELS_NAMES:
        label_search_string = WEB_LABEL_SEARCH_STRING[website][label_name]
        new_val = search_in_text(url_page_text, label_search_string)
        if new_val is not None:
            if label_name == 'tendency':
                new_val = 1.0 if new_val == 'Rising' else -1.0 if new_val == 'Falling' else 0.0
            elif label_name == 'condition':
                new_val = 0.0
            else:
                multiplier = 1.0 if label_name not in WEB_LABEL_MULTIPLIER[website] else WEB_LABEL_MULTIPLIER[website][label_name]
                new_val = round(float(new_val) * multiplier, 3)
        elif label_name == 'wind' or label_name == 'visibility':
            new_val = 0.0
        else:
            print_log("WARNING", f"To validate missed {label_name}, see url:")
            print(url)
        label[label_name] = new_val
    return label
