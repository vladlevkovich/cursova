import time
import cv2
import os
from deepface import DeepFace
from pprint import pprint


def save_face(frame, x, y, w, h):
    face = frame[y:y+h, x:x+w]      # виділяємо область під обличчя
    timestamp = time.strftime('%Y%m%d-%H%M%S')
    face_filename = f'detected_faces/face_{timestamp}.jpg'
    cv2.imwrite(face_filename, face)
    return face


def face_cup():
    cascade_path = 'filters/haarcascade_frontalface_default.xml'
    clf = cv2.CascadeClassifier(cascade_path)
    camera = cv2.VideoCapture(0)
    last_capture_time = time.time()     # час збереження останнього фото
    capture_interval = 5   # інтервал збереження

    while True:
        # зчитуємо дані з камери
        _, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # знаходимло обличчя
        faces = clf.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE
        )
        current_time = time.time()
        if current_time - last_capture_time >= capture_interval:
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
                save_face(frame=frame, x=x, y=y, w=w, h=h)
            last_capture_time = current_time
                # face_id += 1
            #     face = frame[y:y+h, x:x+w]  # виділяємо область під обличчя
            #     face_filename = f'detected_faces/face_{face_id}.jpg'
            #     cv2.imwrite(face_filename, face)
            #     face_id += 1
            #
        cv2.imshow('Faces', frame)

        if cv2.waitKey(1) == 'q':
            break
    camera.release()
    cv2.destroyAllWindows()


def compare_faces(face1_path: str, face2_path: str):
    # рівнюємо обличчя
    result = DeepFace.verify(img1_path=face1_path, img2_path=face2_path, enforce_detection=False)
    pprint(result)
    return result['verified']   # якшо true то обличчя співпадають якшо false то не співпадають


def main():
    # face_cup()
    compare_faces('faces/face_20240919-132452.jpg', 'detected_faces/face_0.jpg')


if __name__ == '__main__':
    main()

