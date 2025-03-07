
# ======================
# LABEL CONSTANTS
# ====================

WEB_LABELS_NAMES = ['temperature', 'pressure', 'humidity', 'wind', 'dewpoint']
LABEL_NAMES = ['date', 'time', 'latitude', 'longitude', 'elevation'] + WEB_LABELS_NAMES + ['sun_direction', 'sun_altitude']
LABEL_FILE_FIELDS = ['video_id', 'year', 'month', 'day', 'hour', 'minute', 'second'] + LABEL_NAMES

NUM_LABELS = len(LABEL_NAMES)
NUM_LABEL_FILE_FIELDS = len(LABEL_FILE_FIELDS)
NUM_LABEL_FILE_NON_LABELS = NUM_LABEL_FILE_FIELDS - NUM_LABELS

# ======================
# LMDB CONSTANTS
# ====================

LMDB_METADATA_SUFFIXES = [b':label', b':quality', b':stillness']

# ======================
# OTHER CONSTANTS
# ====================

LOG_COLORS = {
    "INFO": "\033[95m",
    "OKAY": "\033[92m",
    "WARNING": "\033[93m",
    "ERROR": "\033[91m",
    "END": "\033[0m"
}
