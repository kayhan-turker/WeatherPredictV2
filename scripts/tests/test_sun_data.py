from scripts.scraping.labels.collect_labels import *
from scripts.scraping.labels.request_video_still import *

TORONTO_COORDS = [43.655, -79.383]

print(LABEL_NAMES)
print(collect_labels(datetime.now(), 'CANADA', TORONTO_COORDS[0], TORONTO_COORDS[1]))
print(collect_labels(datetime.now(), 'UNITED STATES', 41, -80))

print(collect_labels(datetime.now(), 'CANADA', 42.293, -83.051))
print(collect_labels(datetime.now(), 'UNITED STATES', 42.3329, -83.0478))

print(get_stream_url("K5ZEJWCTSzQ"))
