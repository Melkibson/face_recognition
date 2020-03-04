import cv2
import pyzbar.pyzbar as pyzbar
from api import get_qrcode


def qr_code_reader(code):
    camera = cv2.VideoCapture(0)
    capture = True
    while capture:
        ret, frame = camera.read()
        decodedObjects = pyzbar.decode(frame)
        while decodedObjects:
            decoded = decodedObjects[0].data
            if decoded == bytes(code, 'utf-8'):
                print("Access granted")
                break
            else:
                print("Access denied")

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


code = get_qrcode()
qr_code_reader(code)

