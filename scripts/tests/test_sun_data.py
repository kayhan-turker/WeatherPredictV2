from scripts.scraping.labels.windy.request_labels_windy import *
from scripts.scraping.labels.source_metadata import *
from scripts.scraping.labels.request_labels import *

# request_sun_data("48.858", "2.294")
# request_weather_data("31.31", "24.294", "2024-02-24T16:20:45.000Z")

print(request_labels('CANADA', 44.6, -76))