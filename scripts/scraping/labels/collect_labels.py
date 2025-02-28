from scripts.scraping.labels.request_location_data import *
from scripts.scraping.labels.request_web_labels import *
from scripts.scraping.labels.request_sun_values import *
from scripts.localConfig import *

LABEL_NAMES = ['date', 'time', 'latitude', 'longitude', 'elevation'] + WEB_LABELS_NAMES + ['sun_direction', 'sun_altitude']


def collect_labels(dt, region, latitude, longitude, elevation=None, dt_format=None):
    if isinstance(dt, str):
        dt_format = dt_format if dt_format is not None else get_datetime_format(dt)
        dt = datetime.strptime(dt, dt_format)
    date = round(get_decimal_year(dt) - dt.year, 4)
    time = round(get_decimal_day(dt), 4)

    elevation = elevation if elevation is not None else request_location_data(latitude, longitude)['elevation']

    labels = [date, time, latitude, longitude, elevation]
    labels += list(request_web_labels(region, latitude, longitude).values())
    labels += request_sun_values(latitude, longitude)

    return labels


def write_label_to_file(source_id, dt, labels):
    label_output = f"{source_id};{datetime.strftime(dt, '%Y;%m;%d;%H;%M;%S')};{';'.join([str(label) for label in labels])}"
    with open(f"{LABEL_SAVE_PATH}{source_id}.txt", "a") as file:
        file.write(f"{label_output}\n")
    print_log("INFO", f"Saved label data: {label_output}")
