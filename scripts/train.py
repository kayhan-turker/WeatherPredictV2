import torchvision.transforms as transforms
from scripts.data_processing.label_statistics import *
from scripts.data_processing.datasets import *
from scripts.localConfig import *


def training_loop(num_epoch, batch_size):

    transform = transforms.Compose([transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    dataset_main = LMDBDataset(LMDB_PATH, transform=transform, quality=None, stillness=None,
                               sun_angle=None, paired=False, pair_same_source_prob=None)
    dataset_pair = LMDBDataset(LMDB_PATH, transform=transform, quality=None, stillness=1,
                               sun_angle=0, paired=True, pair_same_source_prob=1.0)
    train_loader_main = DataLoader(dataset_main, batch_size=batch_size, shuffle=True, num_workers=NUM_CPU_WORKERS, pin_memory=True)
    train_loader_pair = DataLoader(dataset_pair, batch_size=batch_size, shuffle=True, num_workers=NUM_CPU_WORKERS, pin_memory=True)

    label_mean, label_std = calculate_label_stats(LMDB_PATH)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch.backends.cudnn.benchmark = True
    torch.autograd.set_detect_anomaly(False)

    image, label = next(iter(train_loader_main))
    print(label[:, 18])

    image, label, same_source = next(iter(train_loader_pair))
    print(label[:, 18])
    print(same_source)
    print(image.size())


training_loop(1, 32)
