from scripts.utils import *

# Windy url and endpoints
WEBCAM_ENDPOINT = 'https://api.windy.com/webcams/api/v3/webcams/'
webcam_header = {'x-windy-api-key': 'Zfe8zSHc5XpTTQP9m9NHD7a1MxAGAwAP'}
webcam_params = {'include': 'images,location'}


def request_windy_webcam_data(webcam_id):
    response_json = get_url_page_json(f"{WEBCAM_ENDPOINT}{webcam_id}", webcam_header, webcam_params)
    if response_json is None:
        return None, None, None, None

    # return image_url, last_updated_on, latitude, longitude
    return (response_json['images']['current']['preview'], response_json['lastUpdatedOn'],
            response_json['location']['latitude'], response_json['location']['longitude'])
