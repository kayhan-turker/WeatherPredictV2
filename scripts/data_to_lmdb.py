from core.data_processing.create_lmdb import *
from scripts.clear_incomplete_data import *
from common.constants import *
from common.config import *


if CLEAR_INCOMPLETE_DATA_BEFORE_LMDB_WRITE:
    full_data_cleansing()

print_log("INFO", "Pre-processing images and creating lmdb...")
create_lmdb(LMDB_PATH, FILTERED_IMAGES_PATH, LABEL_SAVE_PATH, IMAGE_SIZE)
