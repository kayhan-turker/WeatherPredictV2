from scripts.utils import *


REGIONS = ['CANADA', 'UNITED STATES']
LABELS = ['temp']

REGION_URL = {
    'CANADA': 'https://weather.gc.ca/en/location/index.html?coords=<latitude>,<longitude>',
    'UNITED STATES': 'https://forecast.weather.gov/MapClick.php?lat=<latitude>&lon=<longitude>',
}
LATITUDE_PLACEHOLDER = '<latitude>'
LONGITUDE_PLACEHOLDER = '<longitude>'

LABEL_SEARCH_STRING = {
    'CANADA': {
        'temp': r'Temperature:\</dt\>\<dd [a-z\-0-9]*\>\<span [a-z\-0-9]*\>([\-\.0-9]+)°\</span\>'
    },
    'UNITED STATES': {
        'temp': r'\<p class="myforecast-current-sm"\>9&deg;C\</p\>'
    }
}

# Check for any missing values in dictionaries!

for region, labels in LABEL_SEARCH_STRING.items():
    region_label_search_strings = list(labels.keys())
    for label in LABELS:
        if label not in region_label_search_strings:
            print_log("ERROR", f"Missing label {label} from LABEL_SEARCH_STRING ({region})!")

for region in REGIONS:
    if region not in list(LABEL_SEARCH_STRING.keys()):
        print_log("ERROR", f"Missing region {region} from LABEL_SEARCH_STRING!")

for country, url in REGION_URL.items():
    if LATITUDE_PLACEHOLDER not in url:
        print_log("ERROR", f"Missing latitude placeholder '{LATITUDE_PLACEHOLDER}' from {country} url!")
    if LONGITUDE_PLACEHOLDER not in url:
        print_log("ERROR", f"Missing longitude placeholder '{LONGITUDE_PLACEHOLDER}' from {country} url!")
