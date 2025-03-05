from scripts.utils import *


# Sunrise sunset url
SUNRISE_SUNSET_URL = 'https://www.timeanddate.com/sun/@'
SUN_DIRECTION_FORMAT = '.*"az":\[\{"e":[0-9e\-\.]*,"p":\[([0-9e\-\.]+),.*'
SUN_ALTITUDE_FORMAT = '.*"alt":\[\{"e":[0-9e\-\.]*,"p":\[([0-9e\-\.]+),.*'


def request_sun_values(latitude, longitude):
    response_text = get_url_page_text(f"{SUNRISE_SUNSET_URL}{latitude},{longitude}")
    direction = round(float(search_in_text(response_text, SUN_DIRECTION_FORMAT)), 2)
    altitude = round(90 - float(search_in_text(response_text, SUN_ALTITUDE_FORMAT)), 2)

    direction = round(direction % 360, 2)
    altitude = round((altitude + 180) % 360 - 180, 2)

    return direction, altitude
