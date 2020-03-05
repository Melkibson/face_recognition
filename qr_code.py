import cv2
import pyzbar.pyzbar as pyzbar


def qr_code_reader():
    camera = cv2.VideoCapture(0)
    capture = True
    while capture:
        ret, frame = camera.read()
        decodedObjects = pyzbar.decode(frame)
        while decodedObjects:
            decoded = decodedObjects[0].data
            return decoded
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


qr_code_reader()

