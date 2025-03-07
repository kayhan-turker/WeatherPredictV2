import shutil

from common.localConfig import *
from common.utils import *


def check_label_image_exists(auto_remove=False):
    # Go through label files to ensure all images are present
    for label_file in os.listdir(LABEL_SAVE_PATH):
        if label_file.endswith('.txt'):
            label_file_path = os.path.join(LABEL_SAVE_PATH, label_file)
            source_id = label_file.split('.')[0]

            with open(label_file_path, 'r') as file:
                lines = file.readlines()

            filtered_lines = []
            for line in lines:
                if line.strip():
                    values = line.split(';')
                    image_file = f"{values[1]}-{values[2]}-{values[3]}-{values[4]}-{values[5]}-{values[6]}.jpg"

                    unfiltered_image_file_path = os.path.join(f"{STREAM_IMAGE_SAVE_PATH}{source_id}/", image_file)
                    filtered_image_file_path = os.path.join(f"{LMDB_SOURCE_IMAGE_PATH}{source_id}/", image_file)
                    image_missing = (not os.path.exists(unfiltered_image_file_path) and
                                     not os.path.exists(filtered_image_file_path))

                    if image_missing:
                        print_log("ERROR", f"Missing image file from source {source_id}: {image_file}.")
                        if auto_remove:
                            print_log("INFO", f"Removing label...")
                    elif auto_remove:
                        filtered_lines.append(line)

            # Only write changes if auto remove was enabled
            if auto_remove:
                with open(label_file_path, 'w') as file:
                    file.writelines(filtered_lines)


def check_label_complete(auto_remove=False):
    for label_file in os.listdir(LABEL_SAVE_PATH):
        if label_file.endswith('.txt'):
            label_file_path = os.path.join(LABEL_SAVE_PATH, label_file)

            with open(label_file_path, 'r') as file:
                lines = file.readlines()

            filtered_lines = []
            for line in lines:
                if line.strip():
                    values = line.split(';')
                    skip_line = False
                    for value in values:
                        if value == 'None' or value == '' or value is None:
                            skip_line = True

                    if skip_line:
                        datetime_str = ('-'.join(value for value in values[1:7]))
                        print_log("ERROR", f"Label values missing in {label_file} ({datetime_str}).")

                        if auto_remove:
                            print_log("INFO", f"Removing label...")

                            # If there's a corresponding image, delete it
                            image_file_path = os.path.join(f"{STREAM_IMAGE_SAVE_PATH}{label_file}/", f"{datetime_str}.jpg")
                            if os.path.exists(image_file_path):
                                print_log("INFO", f"Removing unfiltered image...")
                                os.remove(image_file_path)
                            image_file_path = os.path.join(f"{LMDB_SOURCE_IMAGE_PATH}{label_file}/", f"{datetime_str}.jpg")
                            if os.path.exists(image_file_path):
                                print_log("INFO", f"Removing filtered image...")
                                os.remove(image_file_path)

                    # If not skipped, add it to the filtered list to be written
                    elif auto_remove:
                        filtered_lines.append(line)

            # Only write changes if auto remove was enabled
            if auto_remove:
                with open(label_file_path, 'w') as file:
                    file.writelines(filtered_lines)


def check_image_label_exists(image_folder_path, auto_remove=False):
    # Go through image files to make sure all labels are present

    auto_remove_sources = False
    for source_id in os.listdir(image_folder_path):
        source_folder_path = f"{image_folder_path}{source_id}/"

        label_file = f"{source_id}.txt"
        label_file_path = os.path.join(LABEL_SAVE_PATH, label_file)

        if os.path.exists(label_file_path):
            with open(label_file_path, 'r') as file:
                label_file_images = set('-'.join(line.split(';')[1:7]) + '.jpg' for line in file.readlines())
        elif os.path.exists(source_folder_path):
            print_log("ERROR", f"Missing label file for source {source_id}.")
            response = input("Do you want to remove all the contents of the source? (Y/N) Press A to auto-confirm Y: ").strip().lower() \
                if not auto_remove_sources else 'y'
            if response == 'y' or response == 'a':
                print(f"Removing source {source_id} files.")
                shutil.rmtree(source_folder_path)
                if response == 'a':
                    auto_remove_sources = True
            else:
                print("Did not remove source.")
            continue

        for image_file in os.listdir(source_folder_path):
            if image_file not in label_file_images:
                print_log("ERROR", f"Missing label for image {image_file} from source {source_id}.")

                if auto_remove:
                    print_log("INFO", f"Removing image...")
                    image_file_path = os.path.join(source_folder_path, image_file)
                    os.remove(image_file_path)


def full_data_cleansing():
    print_log("INFO", "Checking label completion...")
    check_label_complete(True)
    print_log("INFO", "Checking if label images exist...")
    check_label_image_exists(True)
    print_log("INFO", "Checking if image labels exist...")
    check_image_label_exists(STREAM_IMAGE_SAVE_PATH, True)
    check_image_label_exists(LMDB_SOURCE_IMAGE_PATH, True)
