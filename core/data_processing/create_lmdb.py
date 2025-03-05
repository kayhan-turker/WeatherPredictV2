import lmdb
from tqdm import tqdm
from core.data_processing.preprocessing import *
from core.metadata.video_source_metadata import *


def create_lmdb(lmdb_path, image_folder, label_folder, target_size):
    with lmdb.open(lmdb_path, map_size=int(2e10)) as env:
        source_ids = [source_dir for source_dir in os.listdir(image_folder)
                      if os.path.isdir(os.path.join(image_folder, source_dir))]
        video_metadata, _ = init_video_metadata_manager()

        with env.begin(write=True) as txn:
            for source_id in tqdm(source_ids):
                source_image_folder = os.path.join(image_folder, source_id)
                source_label_file = os.path.join(label_folder, f"{source_id}.txt")

                # Log the quality and stillness state of the source
                quality = video_metadata[source_id]["quality"]
                stillness = video_metadata[source_id]["stillness"]
                txn.put(source_id.encode() + b':quality', str(quality).encode())
                txn.put(source_id.encode() + b':stillness', str(stillness).encode())

                # Read the labels
                with open(source_label_file, 'r') as file:
                    label_records = file.readlines()

                sorted_images = sorted(os.listdir(source_image_folder))
                sorted_label_records = sorted(label_records)
                for image_name, label in zip(sorted_images, sorted_label_records):
                    image_path = os.path.join(source_image_folder, image_name)
                    image = preprocess_image(image_path, target_size)
                    image_bytes = cv2.imencode('.jpg', image)[1].tobytes()

                    # Store image and its label into LMDB
                    key = f"{source_id}:{image_name}".encode()
                    txn.put(key, image_bytes)
                    txn.put(key + b':label', label.strip().encode())



