import cv2
import numpy as np
from json import dumps as dp
from json import loads as ld
import os
from pickle import load

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

face_id = load(open("save.p", "rb"))
names = ['Yamna']
# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
for name in names:
    json = {'id': face_id, 'name': name}
    users = dp(json)
    data = ld(users)
    # Define min window size to be recognized as a face
    minW = 0.5 * cam.get(3)
    minH = 0.5 * cam.get(4)

    while True:

        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.5,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            face_id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            # Check if confidence is less than 100 ==> "0" is perfect match
            if confidence < 100:
                face_id = data['name']
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                face_id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))

            cv2.putText(img, str(face_id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
