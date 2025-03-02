import random
import numpy as np
from scripts.data_processing.create_lmdb import *


def _get_image_source(image_key):
    return image_key.decode().split('_')[0]


def _get_image_metadata(image_key, metadata, txn):
    return txn.get(f"{image_key.decode()}_{metadata}".encode()).decode()


class SourceSampler:
    def __init__(self, lmdb_path, label_mean, label_std, min_quality=None, static=None, min_sun_altitude=None, same_source_prob=None):
        self.env = lmdb.open(lmdb_path, readonly=True)
        self.label_mean = label_mean
        self.label_std = label_std

        self.min_quality = min_quality
        self.static = static
        self.min_sun_altitude = min_sun_altitude
        self.same_source_prob = same_source_prob

        self.image_keys = self._load_keys()
        self.num_sources = self._count_source()

    def _load_keys(self):
        filtered_keys = []
        with (self.env.begin() as txn):
            # Filter out metadata keys (labels, quality, static)
            image_keys = [key for key, _ in txn.cursor() if not any(key.endswith(suffix) for suffix in LMDB_METADATA_SUFFIXES)]

            # Filter based on quality and static needs
            for key in image_keys:
                quality = int(_get_image_metadata(key, 'quality', txn))
                static = int(_get_image_metadata(key, 'static', txn))
                labels = _get_image_metadata(key, 'labels', txn)
                sun_altitude = labels.split(';')[18]

                if (self.min_quality is None or quality >= self.min_quality) and \
                   (self.static is None or static == self.static) and \
                   (self.min_sun_altitude is None or float(sun_altitude) >= self.min_sun_altitude):
                    filtered_keys.append(key)

        return filtered_keys

    def _count_source(self):
        sources = set()
        with self.env.begin() as txn:
            for key, _ in txn.cursor():
                if not any(key.endswith(suffix) for suffix in LMDB_METADATA_SUFFIXES):
                    source = _get_image_source(key)
                    sources.add(source)

        return len(sources)

    def sample_image_key(self):
        return random.choice(self.image_keys)

    def sample_image_key_pair(self):
        if self.num_sources == 1 or (self.same_source_prob is not None and random.random() < self.same_source_prob):
            key_0 = random.choice(self.image_keys)
            source = _get_image_source(key_0)
            same_source_keys = [k for k in self.image_keys if _get_image_source(k) == source]
            key_1 = random.choice(same_source_keys)
            same_source = 1
        else:
            key_0, key_1 = random.sample(self.image_keys, 2)
            while _get_image_source(key_0) == _get_image_source(key_1):
                key_0, key_1 = random.sample(self.image_keys, 2)
            same_source = 0

        return key_0, key_1, same_source

    def get_data(self, key):
        with self.env.begin() as txn:
            image_bytes = txn.get(key)
            image = cv2.imdecode(np.frombuffer(image_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
            label = _get_image_metadata(key, 'labels', txn)

        normalized_label = (label - self.label_mean) / self.label_std
        return image, normalized_label
