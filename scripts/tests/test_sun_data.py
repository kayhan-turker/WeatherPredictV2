from PIL import Image
from scripts.data_processing.source_sampler import *


sampler_main = SourceSampler(LMDB_PATH)
sampler_quality = SourceSampler(LMDB_PATH, 1)
sampler_static = SourceSampler(LMDB_PATH, None, 1)
sampler_day = SourceSampler(LMDB_PATH, None, None, 0)
sampler_same_source = SourceSampler(LMDB_PATH, None, None, None, 1.0)

print("MAIN SAMPLER")
for i in range(3):
    key = sampler_main.sample_image_key()
    print(key)
    image, labels = sampler_main.get_data(key)
    print(labels)
    Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).show()
    input("Press Enter to continue...")

print("QUALITY SAMPLER")
for i in range(3):
    key = sampler_quality.sample_image_key()
    print(key)
    image, labels = sampler_quality.get_data(key)
    print(labels)
    Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).show()
    input("Press Enter to continue...")

print("STATIC SAMPLER")
for i in range(3):
    key = sampler_static.sample_image_key()
    print(key)
    image, labels = sampler_static.get_data(key)
    print(labels)
    Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).show()
    input("Press Enter to continue...")

print("DAY SAMPLER")
for i in range(3):
    key = sampler_day.sample_image_key()
    print(key)
    image, labels = sampler_day.get_data(key)
    print(labels)
    Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).show()
    input("Press Enter to continue...")

print("SAME SOURCE SAMPLER")
for i in range(3):
    key1, key2, same_source = sampler_same_source.sample_image_key_pair()
    print(key1, key2, same_source)
    image1, labels1 = sampler_same_source.get_data(key1)
    image2, labels2 = sampler_same_source.get_data(key2)
    print(labels1)
    print(labels2)
    Image.fromarray(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)).show()
    Image.fromarray(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)).show()
    input("Press Enter to continue...")
