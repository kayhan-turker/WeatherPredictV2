from scripts.data_processing.source_sampler import *
from scripts.data_processing.label_statistics import *


#mean, std = calculate_label_stats(LMDB_PATH)

img1 = np.ones((3, 48, 32))
img2 = np.ones((3, 48, 32))

print(np.stack((img1, img2)).shape)
print(np.concatenate((img1, img2), axis=0).shape)

