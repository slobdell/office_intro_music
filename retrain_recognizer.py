from predict_faces_live import train_recognizer, RECOGNIZER_FILENAME
import cv2


if __name__ == "__main__":
    recognizer = cv2.createFisherFaceRecognizer()
    recognizer = train_recognizer(recognizer)
    recognizer.save(RECOGNIZER_FILENAME)
