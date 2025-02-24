from scripts.scraping.labels.source_metadata import *


def request_web_labels(region, latitude, longitude):
    website = REGION_WEBSITES[region]
    url = WEBSITE_URLS[website].replace(LATITUDE_PLACEHOLDER, str(latitude)).replace(LONGITUDE_PLACEHOLDER, str(longitude))
    url_page_text = get_url_page_text(url)

    labels = {}
    for label, label_search_string in WEB_LABEL_SEARCH_STRING[website].items():
        new_val = search_in_text(url_page_text, label_search_string)
        if new_val is not None:
            new_val = round(float(new_val) * WEB_LABEL_MULTIPLIER[website][label], 2)
        labels[label] = new_val

    return labels
