from scripts.data_processing.source_sampler import *
from scripts.data_processing.label_statistics import *


def training_loop(lmdb_path, num_epoch, batch_size):

    label_mean, label_std = calculate_label_stats(LMDB_PATH)

    sampler_main = SourceSampler(lmdb_path, label_mean, label_std, 1)
    sampler_pair = SourceSampler(LMDB_PATH, label_mean, label_std, 0, 1, -20, 0.5)
