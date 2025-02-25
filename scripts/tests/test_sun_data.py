from scripts.scraping.labels.label_manager import *
from scripts.scraping.youtube.request_youtube_webcams import *

TORONTO_COORDS = [43.655, -79.383]

print(LABEL_NAMES)
print(get_labels(datetime.now(), 'CANADA', TORONTO_COORDS[0], TORONTO_COORDS[1]))
print(get_labels(datetime.now(), 'UNITED STATES', 41, -80))

print(get_labels(datetime.now(), 'CANADA', 42.293, -83.051))
print(get_labels(datetime.now(), 'UNITED STATES', 42.3329, -83.0478))

print(get_stream_url("K5ZEJWCTSzQ"))
