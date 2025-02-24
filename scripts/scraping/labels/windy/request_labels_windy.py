from scripts.utils import *

WEATHER_ENDPOINT = 'https://api.windy.com/api/point-forecast/v2'
reading_header = {'x-windy-api-key': 'UIzU9eanZJYRSzegwtJdezIYSMgPBClc'}


def request_weather_data(latitude, longitude, in_datetime):
    request_body = {
        "lat": latitude,
        "lon": longitude,
        "model": "gfs",
        "parameters": ["temp", "dewpoint", "precip", "wind", "lclouds", "mclouds", "hclouds", "rh"],
        "levels": ["surface"],
        "key": "UIzU9eanZJYRSzegwtJdezIYSMgPBClc"
    }

    response = requests.post(WEATHER_ENDPOINT, json=request_body, headers=reading_header)

    if response.status_code != 200:
        print_log("ERROR", f"Weather data for latitude {latitude} and longitude {longitude} not valid!")
        return None

    response_json = response.json()
    print(response_json)
