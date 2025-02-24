from scripts.scraping.labels.source_metadata import *


def request_labels(region, latitude, longitude):
    url = REGION_URL[region].replace(LATITUDE_PLACEHOLDER, str(latitude)).replace(LONGITUDE_PLACEHOLDER, str(longitude))
    url_page_text = get_url_page_text(url)

    labels = {}
    for label_name, label_search_string in LABEL_SEARCH_STRING[region].items():
        labels[label_name] = search_in_text(url_page_text, label_search_string)

    return labels
