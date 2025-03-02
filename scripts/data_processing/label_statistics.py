import lmdb
import numpy as np
from scripts.constants import *


def calculate_label_stats(lmdb_path):
    env = lmdb.open(lmdb_path, readonly=True)
    label_records = []

    with env.begin() as txn:
        # Iterate over all keys and extract labels
        for key, value in txn.cursor():
            if key.endswith(b'_label'):  # Check if the key is a label
                label = value.decode().split(';')[len(DATA_FILE_FIELDS) - len(LABEL_NAMES):]
                label = [float(x) for x in label]  # Convert label to float
                label_records.append(label)

    # Convert labels to a NumPy array
    label_records = np.array(label_records)

    # Calculate mean and standard deviation
    mean = np.mean(label_records, axis=0)
    std = np.std(label_records, axis=0)

    return mean, std
