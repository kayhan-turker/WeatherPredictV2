from scripts.utils import *


# Sunrise sunset url
SUNRISE_SUNSET_URL = 'https://www.timeanddate.com/sun/@'
DIRECTION_FORMAT = '.*"az":\[\{"e":[0-9]*,"p":\[([0-9.]+),.*'
ALTITUDE_FORMAT = '.*"alt":\[\{"e":[0-9]*,"p":\[([0-9.]+),.*'


def request_sun_data(latitude, longitude):
    response_text = get_url_page_text(f"{SUNRISE_SUNSET_URL}{latitude},{longitude}")
    direction = search_in_text(response_text, DIRECTION_FORMAT)
    altitude = search_in_text(response_text, ALTITUDE_FORMAT)

    return direction, altitude
