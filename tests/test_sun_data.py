from core.data_processing.data_cleansing import *
from core.data_processing.label_statistics import *

full_data_cleansing()

#mean, std = calculate_label_stats(LMDB_PATH)

img1 = np.ones((3, 48, 32))
img2 = np.ones((3, 48, 32))

print(np.stack((img1, img2)).shape)
print(np.concatenate((img1, img2), axis=0).shape)

