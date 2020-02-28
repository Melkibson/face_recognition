import picamera
import numpy as np
import pyzbar.pyzbar as pyzbar

DEVICE = '/dev/video0'
SIZE = (640, 480)

user_code = 'http://google.fr'


def qr_code_reader():
    camera = picamera.PiCamera()
    camera.resolution = (320, 240)
    output = np.empty((240, 320, 3), dtype=np.uint8)

    capture = True
    while capture:
        img = camera.capture(output, format="rgb")
        decodedObjects = pyzbar.decode(img)

        for obj in decodedObjects:
            print("Type:", obj.type)
            print("Data: ", obj.data, "\n")


qr_code_reader()



