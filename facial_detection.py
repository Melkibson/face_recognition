import cv2
import os
from pickle import dump

cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video width
cam.set(4, 480)  # set video height
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# For each person, enter one numeric face id
face_id = int.from_bytes(os.urandom(3), byteorder='little') % 9999999999
dump(face_id, open("save.p", "wb"))

print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count
count = 0
while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        count += 1
        # Save the captured image into the datasets folder
        user_directory = "training-data/user_" + str(face_id)
        try:
            os.stat(user_directory)
        except:
            os.makedirs(user_directory)

        user_data_path = user_directory + "/User." + str(face_id) + '.' + str(count) + ".jpg"
        cv2.imwrite(user_data_path, gray[y:y + h, x:x + w])
        cv2.imshow('image', img)
    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break
    elif count >= 1:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
