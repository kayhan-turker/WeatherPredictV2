from scripts.scraping.labels.label_manager import *

TORONTO_COORDS = [43.655, -79.383]

print(LABEL_NAMES)
print(get_labels(datetime.now(), 'CANADA', TORONTO_COORDS[0], TORONTO_COORDS[1]))
