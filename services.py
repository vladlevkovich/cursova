import cv2
import os

def cup_image(img_path, cropped_photo_path):
    """шукаємо обличчя на фото"""
    try:
        cascade_path = 'filters/haarcascade_frontalface_default.xml'
        if not os.path.exists(img_path):
            print(f"Файл за шляхом {img_path} не знайдено.")
            return 'Файл не знайдено'
        print(img_path)
        image = cv2.imread(f'{img_path}')
        face_cascade = cv2.CascadeClassifier(cascade_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        if len(faces) != 0:
            for (x, y, w, h) in faces:
                face = image[y:y+h, x:x+w]
                cv2.imwrite(cropped_photo_path, face)
                break
            return 'Збережено'
        else:
            return 'Обличчя не знайдено'
    except Exception as e:
        return e


def check_face():
    pass
