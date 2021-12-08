
import cv2
import numpy as np
from keras.models import load_model

model = load_model("core/mask-detect-model")
rect_size = 4
haarcascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def get_faces(img):
    rerect_size = cv2.resize(
        img, (img.shape[1] // rect_size, img.shape[0] // rect_size))
    return haarcascade.detectMultiScale(rerect_size)


def mask_detection_util(img):
    detected = []
    faces = get_faces(img)
    has_mask = False

    for f in faces:
        (x, y, w, h) = [v * rect_size for v in f]

        face_img = img[y:y+h, x:x+w]
        rerect_sized = cv2.resize(face_img, (150, 150))
        normalized = rerect_sized/255.0
        reshaped = np.reshape(normalized, (1, 150, 150, 3))
        reshaped = np.vstack([reshaped])
        result = model.predict(reshaped)

        label = np.argmax(result, axis=1)[0]
        if label == 1:
            has_mask = True

        detected.append(
            {'label': label, 'x': x, 'y': y, 'w': w, 'h': h})

    return detected, has_mask


def mask_detection(img):
    img = cv2.imdecode(np.fromstring(
        img.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    detected, has_mask = mask_detection_util(img)
    detected_flip, has_mask_flip = mask_detection_util(cv2.flip(img, 1, 1))

    if has_mask:
        return detected
    if has_mask_flip:
        return detected_flip
    if len(detected) > 0:
        return detected

    return detected_flip


def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()
