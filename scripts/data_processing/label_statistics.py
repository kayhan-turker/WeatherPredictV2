import lmdb
import numpy as np
from scripts.constants import *


def calculate_label_stats(lmdb_path):
    env = lmdb.open(lmdb_path, readonly=True)
    label_records = []

    with env.begin() as txn:
        # Iterate over all keys and extract labels
        for key, value in txn.cursor():
            if key.endswith(b'_labels'):  # Check if the key is a label
                labels = value.decode().split(';')[len(DATA_FILE_FIELDS) - len(LABEL_NAMES):]
                labels = [float(label) for label in labels]  # Convert label to float
                label_records.append(labels)

    # Convert labels to a NumPy array
    label_records = np.array(label_records)

    # Calculate mean and standard deviation
    mean = np.mean(label_records, axis=0)
    std = np.std(label_records, axis=0)

    return mean, std
