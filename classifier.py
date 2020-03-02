import os
from os import listdir, path
import face_recognition
import numpy as np
import cv2
import time
import datetime
import pygame
import pygame.camera
from pygame.locals import *

# initialize the camera and grab a reference to the raw camera capture
pygame.init()
pygame.camera.init()

# Get a reference to webcam #0 (the default one)
screen = pygame.display.set_mode(640, 480 )
camlist = pygame.camera.list_cameras()
cam = pygame.camera.Camera(camlist[0], (640, 480))
cam.start()

known_face_encodings = []
# Get list of users directories names
dir_path = 'training-data'
dir_name = listdir(dir_path)
user_faces_name = np.append([], dir_name)


# Encode all users
def all_face_encoding():
    # Get list of users directories names
    all_user = np.append([], listdir('training-data'))
    for user in all_user:
        #  if path.exists("training-data/{0}/{1}_encoding2.txt".format(name, name)):
        # effacer image encoding et rename face encoding2 en encoding
        if path.exists("training-data/{0}/{1}.jpg".format(user, user)):
            user_image = face_recognition.load_image_file("training-data/{0}/{1}.jpg".format(user, user))
            user_face_encoding = face_recognition.face_encodings(user_image)[0]
            if path.exists('training-data/{0}/{1}_encoding.txt'.format(user, user)):
                os.remove('training-data/{0}/{1}_encoding.txt'.format(user, user))
            np.savetxt('training-data/{0}/{1}_encoding.txt'.format(user, user), user_face_encoding)
            os.remove("training-data/{0}/{1}.jpg".format(user, user))
        # load every user
        user_face_encoding = np.loadtxt('training-data/{0}/{1}_encoding.txt'.format(user, user))
        known_face_encodings.append(user_face_encoding)


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
face_log = {}
process_this_frame = True
reset = time.time() + 60 * 60 * 24

all_face_encoding()

while True:
    # grab an image from the camera
    img = cam.get_image()
    screen.blit(img, (0, 0))
    pygame.display.flip()

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Ptdr t ki"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

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
        if not name == 'Ptdr t ki' and not os.path.isfile("training-data/{0}/{1}.jpg".format(name, name)):
            location_for_update = 'training-data/{0}/{1}_encoding.txt'.format(name, name)
            modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(location_for_update))  # remove datetime
            duration = today - modified_date
            if duration.seconds > 30:
                # mettre a jour photo si date > 1 mois
                cv2.imwrite('training-data/{0}/{1}.jpg'.format(name, name), frame)
            os.system("python3 lock_control.py authorized " + name)
        else:
            os.system("python3 lock_control.py unauthorized")
        print(name)

        datestamp = today.strftime("%m/%d/%Y, %H:%M:%S")
        date = today.strftime("%m-%d-%Y")
        if not os.path.exists('log'):
            os.makedirs('log')

        if name not in face_log or time.time() > face_log[name]:
            face_log[name] = time.time() + 10
            mode = 'a' if os.path.isfile("log/" + date) else 'w'
            with open("log/" + date, mode) as log:
                log.write(name + " / face / " + datestamp + "\n")
                log.close()

    if time.time() > reset:
        all_face_encoding()
        reset = time.time() + 60 * 60 * 24

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
