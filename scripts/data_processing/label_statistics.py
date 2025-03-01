import lmdb
import numpy as np
from scripts.constants import *


def calculate_label_stats(lmdb_path):
    env = lmdb.open(lmdb_path, readonly=True)
    labels = []

    with env.begin() as txn:
        # Iterate over all keys and extract labels
        for key, value in txn.cursor():
            if key.endswith(LMDB_METADATA_SUFFIXES['label']):  # Check if the key is a label
                label = float(value.decode())  # Convert label to float
                labels.append(label)

    # Convert labels to a NumPy array
    labels = np.array(labels)

    # Calculate mean and standard deviation
    mean = np.mean(labels)
    std = np.std(labels)

    return mean, std