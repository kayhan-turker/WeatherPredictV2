from scripts.data_processing.clear_incomplete_data import *
from scripts.data_processing.label_statistics import *

print_log("INFO", "Checking label completion...")
check_label_complete(True)
print_log("INFO", "Checking if label images exist...")
check_label_image_exists(True)
print_log("INFO", "Checking if image labels exist...")
check_image_label_exists(True)

#mean, std = calculate_label_stats(LMDB_PATH)

img1 = np.ones((3, 48, 32))
img2 = np.ones((3, 48, 32))

print(np.stack((img1, img2)).shape)
print(np.concatenate((img1, img2), axis=0).shape)

