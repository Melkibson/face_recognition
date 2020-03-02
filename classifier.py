import datetime
import os
import face_recognition
import numpy as np
import cv2
import time

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()
known_face_encodings = []
user_code = 'http://google.fr'

# Get list of users directories names
dir_path = 'training-data'
dir_name = os.listdir(dir_path)
user_faces_name = np.append([], dir_name)


# Encode all users
def all_face_encoding():
    # Get list of users directories names
    all_user = np.append([], os.listdir('training-data'))

    for user in all_user:
        #  if path.exists("training-data/{0}/{1}_encoding2.txt".format(name, name)):
        # effacer image encoding et rename face encoding2 en encoding
        if os.path.exists("training-data/{0}/{1}.jpg".format(user, user)):
            user_image = face_recognition.load_image_file("training-data/{0}/{1}.jpg".format(user, user))
            user_face_encoding = face_recognition.face_encodings(user_image)[0]
            if os.path.exists('training-data/{0}/{1}_encoding.txt'.format(user, user)):
                os.remove('training-data/{0}/{1}_encoding.txt'.format(user, user))
            np.savetxt('training-data/{0}/{1}_encoding.txt'.format(user, user), user_face_encoding)
            os.remove("training-data/{0}/{1}.jpg".format(user, user))
        # load every user
        user_face_encoding = np.loadtxt('training-data/{0}/{1}_encoding.txt'.format(user, user))
        known_face_encodings.append(user_face_encoding)


# update known faces
def face_update(frame, name):
    cv2.imwrite('training-data/{0}/{1}.jpg'.format(name, name), frame)
    all_face_encoding()


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
timeout = time.time() + 60 * 60 * 24
all_face_encoding()

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Ptdr t ki"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = user_faces_name[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        today = datetime.datetime.today()
        font = cv2.FONT_HERSHEY_DUPLEX
        if not name == 'Ptdr t ki' and not os.path.isfile("training-data/{0}/{1}.jpg".format(name, name)):
            location_for_update = 'training-data/{0}/{1}_encoding.txt'.format(name, name)
            modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(location_for_update))
            duration = today - modified_date
            if duration.days > 30:
                # mettre a jour photo si date > 1 mois
                face_update(frame, name)
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        datestamp = today.strftime("%m/%d/%Y, %H:%M:%S")
        date = today.strftime("%m-%d-%Y")
        mode = 'a' if os.path.isfile("log/" + date) else 'w'
        with open("log/" + date, mode) as log:
            log.write(name + " / face / " + datestamp + "\n")
            log.close()

        #QR CODE

        data, bbox, ret = detector.detectAndDecode(frame)
        if data:
            if data == user_code:
                print('Access granted')
            else:
                print('Access denied')

        # Display the resulting image
    cv2.imshow('Video', frame)

    if time.time() > timeout:
        all_face_encoding()
        timeout = time.time() + 60 * 60 * 24

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
