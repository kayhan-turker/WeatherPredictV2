from scripts.utils import *

REGIONS = ['CANADA', 'UNITED STATES']
WEB_LABELS_NAMES = ['temperature', 'pressure', 'humidity', 'wind', 'dewpoint']

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
        'temperature': r'Temperature:\</dt\>\<dd data-v-7e10dc71\>\<span data-v-7e10dc71\>([0-9\.\-]+)°\<',
        'pressure': r'Pressure:\</dt\>\<dd data-v-7e10dc71\> ([0-9\.]+) \<',
        'humidity': r'Humidity:\</dt\>\<dd data-v-7e10dc71\>([0-9\.]+)\<',
        'wind': r'Wind:\</dt\>\<dd data-v-7e10dc71\>\<abbr title="[a-zA-Z\-]+" data-v-7e10dc71\>[A-Z]+\</abbr\> ([0-9\.]+) \<',
        'visibility': r'Visibility:\</dt\>\<dd data-v-7e10dc71\> ([0-9\.]+) \<',
        'dewpoint': r'Dew point:\</dt\>\<dd data-v-7e10dc71\>\<span data-v-7e10dc71\>([0-9\.\-]+)°\<',
        'condition': r'Condition:\</dt\>\<dd data-v-7e10dc71\>\<span data-v-7e10dc71\>([A-Za-z ]+)\<',
        'tendency': r'Tendency:\</dt\>\<dd data-v-7e10dc71\>([A-Za-z ]+)\<',
    },
    'forecast.weather.gov': {
        'temperature': r'\<p class="myforecast-current-sm"\>([0-9\-]+)&deg;C\</p\>',
        'pressure': r'Barometer\</b\>\</td\> \<td\>([0-9\.]+) *in\ *',
        'humidity': r'Humidity\</b\>\</td\> \<td\>([0-9\.]+)\%\<',
        'wind': r'Wind Speed\</b\>\</td\> \<td\>[A-Za-z]+ ([0-9\.\-]+) [A-Za-z]+</td>',
        'visibility': r'Visibility\</b\>\</td\> \<td\>([0-9\.]+) mi\<',
        'dewpoint': r'Dewpoint\</b\>\</td\> \<td\>[0-9\.\-]+&deg;F \(([0-9\-\.]+)&deg;C\)\<',
    }
}

WEB_LABEL_MULTIPLIER = {
    'weather.gc.ca': {
    },
    'forecast.weather.gov': {
        'pressure': 33.86,
        'wind': 1.61,
    }
}

# Check for any missing values in dictionaries!
for website, web_labels_search_strings in WEB_LABEL_SEARCH_STRING.items():
    web_labels = list(web_labels_search_strings.keys())
    for label in WEB_LABELS_NAMES:
        if label not in web_labels:
            print_log("ERROR", f"Missing label {label} from LABEL_SEARCH_STRING ({website})!")

for website in WEBSITE_URLS.keys():
    if website not in list(WEB_LABEL_SEARCH_STRING.keys()):
        print_log("ERROR", f"Missing website {website} from LABEL_SEARCH_STRING!")

for website, url in WEBSITE_URLS.items():
    if LATITUDE_PLACEHOLDER not in url:
        print_log("ERROR", f"Missing latitude placeholder '{LATITUDE_PLACEHOLDER}' from {website} url!")
    if LONGITUDE_PLACEHOLDER not in url:
        print_log("ERROR", f"Missing longitude placeholder '{LONGITUDE_PLACEHOLDER}' from {website} url!")
