from scripts.data_processing.create_lmdb import *
from scripts.data_processing.clear_incomplete_data import *
from scripts.constants import *

CLEAR_INCOMPLETE_DATA = True

if CLEAR_INCOMPLETE_DATA:
    print_log("INFO", "Checking if image labels exist...")
    check_image_label_exists(True)
    print_log("INFO", "Checking label completion...")
    check_label_complete(True)
    print_log("INFO", "Checking if label images exist...")
    check_label_image_exists(True)
    print_log("INFO", "Checking if image labels exist...")
    check_image_label_exists(True)
    print_log("INFO", "Checking label completion...")
    check_label_complete(True)
    print_log("INFO", "Checking if label images exist...")
    check_label_image_exists(True)

print_log("INFO", "Pre-processing images and creating lmdb...")
create_lmdb(LMDB_PATH, STREAM_IMAGE_SAVE_PATH, LABEL_SAVE_PATH, IMAGE_SIZE)
