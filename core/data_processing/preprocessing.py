import cv2


def preprocess_image(image_path, target_size):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    h, w = image.shape[:2]

    short_dim = 0 if w > h else 1
    scaling = target_size / image.shape[short_dim]
    resized_image = cv2.resize(image, (int(round(w * scaling)), int(round(h * scaling))))

    return resized_image
