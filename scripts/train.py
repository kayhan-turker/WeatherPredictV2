from torch.utils.data import DataLoader
from core.data_processing.label_statistics import *
from core.data_processing.datasets import *
from common.localConfig import *
from common.utils import *
from common.config import *


def training_loop(num_epochs, batch_size):

    print_log("INFO", "Initialize datasets...")
    transform = transforms.Compose([transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    dataset_main = LMDBDataset(LMDB_PATH, transform=transform, quality=None, stillness=None,
                               sun_angle=None, paired=False, pair_same_source_prob=None)
    dataset_pair = LMDBDataset(LMDB_PATH, transform=transform, quality=None, stillness=1,
                               sun_angle=0, paired=True, pair_same_source_prob=1.0)

    print_log("INFO", "Initialize data loaders...")
    train_loader_main = DataLoader(dataset_main, batch_size=batch_size, shuffle=True, num_workers=NUM_CPU_WORKERS, pin_memory=True)
    train_loader_pair = DataLoader(dataset_pair, batch_size=batch_size, shuffle=True, num_workers=NUM_CPU_WORKERS, pin_memory=True)

    print_log("INFO", "Calculating label statistics...")
    label_mean, label_std = calculate_label_stats(LMDB_PATH)

    print_log("INFO", "Checking for cuda availability...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print_log("WARNING" if device == 'cpu' else "INFO", f"Using device {device}.")
    torch.backends.cudnn.benchmark = True
    torch.autograd.set_detect_anomaly(False)


training_loop(NUM_EPOCHS, BATCH_SIZE)
