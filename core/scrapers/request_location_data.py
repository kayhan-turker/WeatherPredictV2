from common.utils import *

LOCATION_ELEVATION_URL = 'https://api.open-meteo.com/v1/forecast?latitude=<latitude>&longitude=<longitude>'


def request_location_data(latitude, longitude):
    url = LOCATION_ELEVATION_URL.replace('<latitude>', str(latitude)).replace('<longitude>', str(longitude))
    json_response = get_url_page_json(url, {}, {})
    return json_response
