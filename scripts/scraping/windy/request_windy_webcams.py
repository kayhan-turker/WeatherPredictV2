import os
import requests
from PIL import Image
from io import BytesIO
from scripts.utils import *

# Windy url and endpoints
WEBCAM_ENDPOINT = 'https://api.windy.com/webcams/api/v3/webcams/'
webcam_header = {'x-windy-api-key': 'Zfe8zSHc5XpTTQP9m9NHD7a1MxAGAwAP'}
webcam_params = {'include': 'images,location'}


def request_webcam_data(webcam_id):
    response = requests.get(WEBCAM_ENDPOINT + webcam_id, headers=webcam_header, params=webcam_params)
    if response.status_code != 200:
        print_log("ERROR", f"Webcam Id {webcam_id} not valid!")
        return None, None, None, None

    response_json = response.json()
    # return image_url, last_updated_on, latitude, longitude
    return (response_json['images']['current']['preview'], response_json['lastUpdatedOn'],
            response_json['location']['latitude'], response_json['location']['longitude'])
