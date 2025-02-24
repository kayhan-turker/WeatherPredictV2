from scripts.utils import *

REGIONS = ['CANADA', 'UNITED STATES']
WEB_LABELS = ['temperature', 'pressure']

REGION_WEBSITES = {
    'CANADA': 'weather.gc.ca',
    'UNITED STATES': 'forecast.weather.gov',
}

WEBSITE_URLS = {
    'weather.gc.ca': 'https://weather.gc.ca/en/location/index.html?coords=<latitude>,<longitude>',
    'forecast.weather.gov': 'https://forecast.weather.gov/MapClick.php?lat=<latitude>&lon=<longitude>',
}
LATITUDE_PLACEHOLDER = '<latitude>'
LONGITUDE_PLACEHOLDER = '<longitude>'

WEB_LABEL_SEARCH_STRING = {
    'weather.gc.ca': {
        'temperature': r'Temperature:\</dt\>\<dd [a-z\-0-9]*\>\<span [a-z\-0-9]*\>([\-\.0-9]+)°\<',
        'pressure': r'Pressure:\</dt\>\<dd data-v-7e10dc71\> ([0-9\.]+) \<',
    },
    'forecast.weather.gov': {
        'temperature': r'\<p class="myforecast-current-sm"\>([0-9\-]+)&deg;C\</p\>',
        'pressure': r'\<td\>[0-9\.]+ in \(([0-9\.]+) mb\)\</td\>',
    }
}

WEB_LABEL_MULTIPLIER = {
    'weather.gc.ca': {
        'temperature': 1,
        'pressure': 1,
    },
    'forecast.weather.gov': {
        'temperature': 1,
        'pressure': 0.1,
    }
}

# Check for any missing values in dictionaries!
for dict_search in [WEB_LABEL_SEARCH_STRING, WEB_LABEL_MULTIPLIER]:

    for website, web_labels_search_strings in dict_search.items():
        web_labels = list(web_labels_search_strings.keys())
        for label in WEB_LABELS:
            if label not in web_labels:
                print_log("ERROR", f"Missing label {label} from LABEL_SEARCH_STRING ({website})!")

    for website in WEBSITE_URLS.keys():
        if website not in list(dict_search.keys()):
            print_log("ERROR", f"Missing website {website} from LABEL_SEARCH_STRING!")

for website, url in WEBSITE_URLS.items():
    if LATITUDE_PLACEHOLDER not in url:
        print_log("ERROR", f"Missing latitude placeholder '{LATITUDE_PLACEHOLDER}' from {website} url!")
    if LONGITUDE_PLACEHOLDER not in url:
        print_log("ERROR", f"Missing longitude placeholder '{LONGITUDE_PLACEHOLDER}' from {website} url!")
