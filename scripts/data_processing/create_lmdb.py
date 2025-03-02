import lmdb
from tqdm import tqdm
from scripts.data_processing.preprocessing import *
from scripts.metadata.video_source_metadata import *
from scripts.constants import *


def create_lmdb(source_folder, label_folder, lmdb_path, target_height):
    env = lmdb.open(lmdb_path, map_size=int(2e10))
    sources = [d for d in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, d))]

    with env.begin(write=True) as txn:
        for source in tqdm(sources):
            source_image_folder = os.path.join(source_folder, source)
            source_label_file = os.path.join(label_folder, f"{source}.txt")

            with open(source_label_file, 'r') as file:
                label_records = file.readlines()

            sorted_images = sorted(os.listdir(source_image_folder))
            sorted_label_records = sorted(label_records)
            for image_name, labels in zip(sorted_images, sorted_label_records):
                image_path = os.path.join(source_image_folder, image_name)
                image = preprocess_image(image_path, target_height)
                image_bytes = cv2.imencode('.jpg', image)[1].tobytes()

                # Store image and labels into LMDB
                key = f"{source}_{image_name}".encode()
                quality = video_source_metadata[source]["quality"]
                static = video_source_metadata[source]["static"]

                txn.put(key, image_bytes)
                txn.put(key + b'labels', labels.strip().encode())
                txn.put(key + b'quality', str(quality).encode())
                txn.put(key + b'static', str(static).encode())



