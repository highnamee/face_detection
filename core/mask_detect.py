
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


def mask_detection(img):
    detected = []
    img = cv2.imdecode(np.fromstring(
        img.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    faces = get_faces(img)

    if(len(faces) == 0):
        img = cv2.flip(img, 1, 1)
        faces = get_faces(img)

    for f in faces:
        (x, y, w, h) = [v * rect_size for v in f]

        face_img = img[y:y+h, x:x+w]
        rerect_sized = cv2.resize(face_img, (150, 150))
        normalized = rerect_sized/255.0
        reshaped = np.reshape(normalized, (1, 150, 150, 3))
        reshaped = np.vstack([reshaped])
        result = model.predict(reshaped)

        label = np.argmax(result, axis=1)[0]

        detected.append(
            {'label': label, 'x': x, 'y': y, 'w': w, 'h': h})

    return detected


def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()
