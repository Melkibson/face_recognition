#!/usr/bin/env python
# coding: utf-8

import sys
import time
# import RPi.GPIO as GPIO
#
# import dothat.lcd as lcd
# import dothat.backlight as backlight

import os
from os import path, listdir

import numpy as np
import cv2
import face_recognition

import datetime
import time

import threading

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
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


# def lock_control(argument, identifiant):
#
#     # declare LCD display
#     lcd.clear()
#
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(18, GPIO.OUT)
#     r = GPIO.PWM(18, 50)
#     r.start(0)
#
#     if argument == "authorized":
#         lcd.write("Bienvenue " + identifiant)
#         backlight.rgb(0, 255, 0)
#         r.ChangeDutyCycle(5)
#         time.sleep(10)
#         backlight.rgb(255, 255, 255)
#         r.ChangeDutyCycle(10)
#         time.sleep(3)
#
#     if argument == "waiting":
#         backlight.rgb(255, 255, 0)
#         time.sleep(2)
#
#     if argument == "unauthorized":
#         backlight.rgb(255, 0, 0)
#         lcd.write("Acces non autorise.")
#         time.sleep(2)
#
#     r.stop()
#     backlight.graph_off()
#     backlight.off()
#     lcd.clear()
#     GPIO.cleanup()


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
face_log = {}
process_this_frame = True
reset = time.time() + 60 * 60 * 24
print("I know you...")
# waiting = threading.Thread(None, lock_control, None, ("waiting", "no"), {})
# waiting.start()
all_face_encoding()

if not os.path.exists('log'):
    os.makedirs('log')

print("Im watching you...")
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Ptdr t ki"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = user_faces_name[best_match_index]
            face_names.append(name)

    process_this_frame = not process_this_frame
    # Display the results
    for name in face_names:
        print(name)
        today = datetime.datetime.today()
        if not name == 'Ptdr t ki' and not os.path.isfile("training-data/{0}/{1}.jpg".format(name, name)):
            location_for_update = 'training-data/{0}/{1}_encoding.txt'.format(name, name)
            modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(location_for_update))  # remove datetime
            duration = today - modified_date
            if duration.days > 30:
                # mettre a jour photo si date > 1 mois
                cv2.imwrite('training-data/{0}/{1}.jpg'.format(name, name), frame)
            # authorized = threading.Thread(None, lock_control, None, ("waiting", name), {})
            # authorized.start()
        # else:
            # unauthorized = threading.Thread(None, lock_control, None, ("waiting", "no"), {})
            # unauthorized.start()
        datestamp = today.strftime("%m/%d/%Y, %H:%M:%S")
        date = today.strftime("%m-%d-%Y")
        if name not in face_log or time.time() > face_log[name]:
            face_log[name] = time.time() + 10
            mode = 'a' if os.path.isfile("log/" + date) else 'w'
            with open("log/" + date, mode) as log:
                log.write(str(name) + " / face / " + str(datestamp) + "\n")
                log.close()

    if time.time() > reset:
        all_face_encoding()
        reset = time.time() + 60 * 60 * 24
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
