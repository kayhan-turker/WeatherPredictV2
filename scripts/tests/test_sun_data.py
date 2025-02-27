from scripts.scraping.labels.collect_labels import *
from scripts.scraping.labels.request_video_still import *

TORONTO_COORDS = [43.655, -79.383]

print(LABEL_NAMES)
print(collect_labels(datetime.now(), 'UNITED STATES', 47.38, -113.92))
print(collect_labels(datetime.now(), 'GLOBAL', 47.38, -113.92))
