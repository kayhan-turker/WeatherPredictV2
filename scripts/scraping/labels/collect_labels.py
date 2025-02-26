from scripts.scraping.labels.request_location_data import *
from scripts.scraping.labels.request_web_labels import *
from scripts.scraping.labels.request_sun_values import *

LABEL_NAMES = ['date', 'time', 'latitude', 'longitude', 'elevation'] + WEB_LABELS_NAMES + ['sun_direction', 'sun_altitude']


def collect_labels(dt, region, latitude, longitude, elevation=None, dt_format=None):
    if isinstance(dt, str):
        dt_format = dt_format if dt_format is not None else get_datetime_format(dt)
        dt = datetime.strptime(dt, dt_format)
    date = round(get_decimal_year(dt) - dt.year, 2)
    time = round(get_decimal_day(dt), 2)

    elevation = elevation if elevation is not None else request_location_data(latitude, longitude)['elevation']

    labels = [date, time, latitude, longitude, elevation]
    labels += list(request_web_labels(region, latitude, longitude).values())
    labels += request_sun_values(latitude, longitude)

    return labels

