from torch.utils.data import Dataset
import random
import lmdb
import cv2
from common.utils import *


def get_image_data(image_key, metadata, txn):
    # If value is from the source system, set key to source_id
    if metadata == b'quality' or metadata == b'stillness':
        image_key = image_key.split(b':')[0]
    return txn.get(image_key + b':' + metadata).decode()


def crop_torch_image(image):
    _, height, width = image.shape
    crop_x = random.randint(0, width - IMAGE_SIZE)
    crop_y = random.randint(0, height - IMAGE_SIZE)
    return image[:, crop_y:crop_y + IMAGE_SIZE, crop_x:crop_x + IMAGE_SIZE]


def lmdb_image_to_torch(image_key, txn):
    image_bytes = txn.get(image_key)
    image_np = cv2.imdecode(np.frombuffer(image_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
    image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    return torch.from_numpy(image_np).permute(2, 0, 1).float() / 255.0


def lmdb_label_to_torch(label_key, txn):
    label_str = txn.get(label_key).decode()
    label = label_str.split(';')[NUM_LABEL_FILE_NON_LABELS:]
    label = [float(x) for x in label]  # Convert label to float
    return torch.tensor(label, dtype=torch.float32)


class LMDBDataset(Dataset):
    def __init__(self, lmdb_path, transform=None, quality=None, stillness=None,
                 sun_angle=None, paired=False, pair_same_source_prob=None):
        self.lmdb_path = lmdb_path

        self.transform = transform
        self.quality = quality
        self.stillness = stillness
        self.sun_angle = sun_angle

        self.paired = paired
        self.pair_same_source_prob = pair_same_source_prob

        self.image_keys = self.get_filtered_keys()
        self.num_sources = self.count_sources()

    def get_filtered_keys(self):
        with lmdb.open(self.lmdb_path, readonly=True, lock=False, readahead=False, meminit=False) as env:
            with env.begin() as txn:
                # Filter out metadata keys (label, quality, stillness)
                return [key for key, _ in txn.cursor()
                        if not any(key.endswith(suffix) for suffix in LMDB_METADATA_SUFFIXES)
                        and (self.quality is None or int(get_image_data(key, b'quality', txn)) >= self.quality)
                        and (self.stillness is None or int(get_image_data(key, b'stillness', txn)) >= self.stillness)
                        and (self.sun_angle is None or float(get_image_data(key, b'label', txn).split(';')[-1]) >= self.sun_angle)]

    def count_sources(self):
        sources = set()
        for image_key in self.image_keys:
            sources.add(image_key.split(b':')[0])

        print_log("INFO", f"Found {len(sources)} sources:")
        return len(sources)

    def __len__(self):
        return len(self.image_keys)

    def get_key_pair(self, image_key_0):
        # If no probability of same source given, random selection from all sources
        if self.pair_same_source_prob is None or self.num_sources == 1:
            image_key_1 = random.choice(self.image_keys)
            same_source = image_key_0.split(b':')[0] == image_key_1.split(b':')[0]
            return image_key_1, same_source

        # If probability given with more than one source, use that to determine if same source used
        if random.random() < self.pair_same_source_prob:
            same_source_keys = [k for k in self.image_keys if k.split(b':')[0] == image_key_0.split(b':')[0]]
            return random.choice(same_source_keys), 1
        else:
            diff_source_keys = [k for k in self.image_keys if k.split(b':')[0] != image_key_0.split(b':')[0]]
            return random.choice(diff_source_keys), 0

    def __getitem__(self, idx):
        image_key_0 = self.image_keys[idx]
        label_key_0 = image_key_0 + b':label'

        with lmdb.open(self.lmdb_path, readonly=True, lock=False, readahead=False, meminit=False) as env:
            with env.begin(write=False) as txn:
                image_0 = lmdb_image_to_torch(image_key_0, txn)
                label_0 = lmdb_label_to_torch(label_key_0, txn)
                image_0 = self.transform(image_0) if self.transform else image_0

                if self.paired:
                    image_key_1, same_source = self.get_key_pair(image_key_0)
                    label_key_1 = image_key_1 + b':label'

                    image_1 = lmdb_image_to_torch(image_key_1, txn)
                    label_1 = lmdb_label_to_torch(label_key_1, txn)
                    image_1 = self.transform(image_1) if self.transform else image_1

        if not self.paired:
            return crop_torch_image(image_0), label_0
        else:
            return (crop_torch_image(torch.concatenate((image_0, image_1), dim=0)),
                    torch.concatenate((label_0, label_1), dim=0), same_source)

