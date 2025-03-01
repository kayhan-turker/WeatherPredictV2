

WEB_LABELS_NAMES = ['temperature', 'pressure', 'humidity', 'wind', 'dewpoint']
LABEL_NAMES = ['date', 'time', 'latitude', 'longitude', 'elevation'] + WEB_LABELS_NAMES + ['sun_direction', 'sun_altitude']
DATA_FILE_FIELDS = ['video_id', 'year', 'month', 'day', 'hour', 'minute', 'second'] + LABEL_NAMES

LMDB_METADATA_SUFFIXES = {'labels': b'_labels', 'quality': b'_quality', 'static': b'_static'}


LOG_COLORS = {
    "INFO": "\033[95m",
    "OKAY": "\033[92m",
    "WARNING": "\033[93m",
    "ERROR": "\033[91m",
    "END": "\033[0m"
}
