from scripts.scraping.labels.request_web_labels import *
from scripts.scraping.labels.request_sun_values import *

LABEL_NAMES = ['date', 'time', 'latitude', 'longitude'] + WEB_LABELS_NAMES + ['sun_direction', 'sun_altitude']


def get_labels(dt, region, latitude, longitude, dt_format=None):
    if isinstance(dt, str):
        dt_format = dt_format if dt_format is not None else get_datetime_format(dt)
        dt = datetime.strptime(dt, dt_format)
    date = round(get_decimal_year(dt) - dt.year, 2)
    time = round(get_decimal_day(dt), 2)

    labels = [date, time, longitude, latitude]
    labels += list(request_web_labels(region, latitude, longitude).values())
    labels += request_sun_values(latitude, longitude)

    return labels

