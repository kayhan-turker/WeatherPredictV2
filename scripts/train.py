from scripts.data_processing.source_sampler import *


def training_loop(lmdb_path, num_epoch, batch_size):
    sampler_main = SourceSampler(lmdb_path, 1)
    sampler_static = SourceSampler(lmdb_path, 0, 1)
    sampler_pair = SourceSampler(LMDB_PATH, None, None, -20, 0.5)

