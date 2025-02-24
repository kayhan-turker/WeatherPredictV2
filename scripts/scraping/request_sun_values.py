import requests

# Sunrise sunset url
SUNRISE_SUNSET_URL = 'https://api.sunrisesunset.io/json'


def request_sun_data(lat, lng):
    response = requests.get(SUNRISE_SUNSET_URL, params={'lat': lat, 'lng': lng})
    print(f"Sun data: {response.json()}")
