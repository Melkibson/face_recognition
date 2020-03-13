#!/usr/bin/.env python
# coding: utf-8

import sys
import time
import RPi.GPIO as GPIO

import dothat.lcd as lcd
import dothat.backlight as backlight
from os import path, listdir, makedirs, remove
import numpy as np
import cv2
import face_recognition
import datetime
import time
import pyzbar.pyzbar as pyzbar
from api_requests import authenticate, compare_qrcode, get_audio, post_log
import threading

known_face_encodings = []
# Get list of users directories names
dir_path = 'training-data'
dir_name = listdir(dir_path)
user_faces_name = np.append([], dir_name)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
r = GPIO.PWM(18, 50)
r.start(0)


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
                remove('training-data/{0}/{1}_encoding.txt'.format(user, user))
            np.savetxt('training-data/{0}/{1}_encoding.txt'.format(user, user), user_face_encoding)
            remove("training-data/{0}/{1}.jpg".format(user, user))
        # load every user
        user_face_encoding = np.loadtxt('training-data/{0}/{1}_encoding.txt'.format(user, user))
        known_face_encodings.append(user_face_encoding)


def lock_control(argument, identifiant):
    # declare LCD display
    lcd.clear()

    if argument == "authorized":
        backlight.rgb(0, 128, 0)
        lcd.write("Bienvenue ")
        lcd.set_cursor_position(0, 1)
        lcd.write(identifiant)
        r.ChangeDutyCycle(5)
        backlight.rgb(0, 128, 0)
        time.sleep(10)
        r.ChangeDutyCycle(0)
        lcd.clear()
        lcd.write("Closing ...")
        r.ChangeDutyCycle(10)
        get_audio("fermeture")
        backlight.rgb(128, 128, 128)
        time.sleep(3)
        r.ChangeDutyCycle(0)
        lcd.write("Finish")

    if argument == "unauthorized":
        backlight.rgb(128, 0, 0)
        lcd.write("Acces")
        lcd.set_cursor_position(0, 1)
        lcd.write("non autorise.")
        time.sleep(0.5)

    backlight.graph_off()
    backlight.off()
    lcd.clear()


def qr_code_reader(code_frame):
    decodedObjects = pyzbar.decode(code_frame)
    while decodedObjects:
        decoded = decodedObjects[0].data
        return decoded


# Initialize some variables
face_locations = []
face_encodings = []
i1 = False
face_names = []
face_log = {}
seen = False
process_this_frame = True
reset = time.time() + 60 * 60 * 24
authorized = threading.Thread(None, lock_control, None, ("authorized", "no"), {})
unauthorized = threading.Thread(None, lock_control, None, ("unauthorized", "no"), {})
# seuil_min = 1.5

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# encode everyone
all_face_encoding()

if not path.exists('log'):
    makedirs('log')

print("I can see you...")
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
            name = "non reconnu"
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

        if not name == 'non reconnu' and not path.isfile("training-data/{0}/{1}.jpg".format(name, name)):
            location_for_update = 'training-data/{0}/{1}_encoding.txt'.format(name, name)
            modified_date = datetime.datetime.fromtimestamp(path.getmtime(location_for_update))  # remove datetime
            duration = today - modified_date
            if duration.days > 30:
                # mettre a jour photo si date > 1 mois
                cv2.imwrite('training-data/{0}/{1}.jpg'.format(name, name), frame)

            if name == seen:  # check if not a false positive

                # coord = face_locations[0]
                # cropped_image = frame[coord[0] * 4:coord[2] * 4, coord[3] * 4:coord[1] * 4]

                # if not i1:
                # RGB_frame = Image.fromarray(cropped_image)
                # i1 = ImageOps.grayscale(RGB_frame)
                # i1 = ImageOps.solarize(i1, threshold=128)

                # i2 = i1
                # RGB_frame = Image.fromarray(cropped_image)
                # i1 = ImageOps.grayscale(RGB_frame)
                # i1 = ImageOps.solarize(i1, threshold=128)
                # assert i1.mode == i2.mode, "Different kinds of images."

                # pairs = zip(i1.getdata(), i2.getdata())
                # if len(i1.getbands()) == 1:
                # for gray-scale jpegs
                # dif = sum(abs(p1 - p2) for p1, p2 in pairs)
                # else:
                # dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

                # ncomponents = i1.size[0] * i1.size[1] * 3
                # dif = round(dif / 255.0 * 100 / ncomponents, 2)
                # print("Difference (percentage) pour " + name + " :", dif)

                # if dif > seuil_min and not dif == 0:

                seen = False

                if not authorized.is_alive():
                    print("ouverture porte")
                    authorized = threading.Thread(None, lock_control, None, ("authorized", name), {})
                    get_audio("ouverture")
                    authorized.start()
            else:
                seen = name

        else:
            if not unauthorized.is_alive() and not authorized.is_alive():
                unauthorized = threading.Thread(None, lock_control, None, ("unauthorized", "no"), {})
                unauthorized.start()

        datestamp = today.strftime("%m/%d/%Y, %H:%M:%S")
        date = today.strftime("%m-%d-%Y")
        if name not in face_log or time.time() > face_log[name]:
            face_log[name] = time.time() + 10
            post_log(str(name), "face")
            mode = 'a' if path.isfile("log/" + date) else 'w'
            with open("log/" + date, mode) as log:
                log.write(str(name) + " / face / " + str(datestamp) + "\n")
                log.close()

    if time.time() > reset:  # > 24H d'éxécution, puis on recharge tout les visages
        timereset = time.time()
        all_face_encoding()
        timereset = time.time() - timereset
        reset = time.time() + 60 * 60 * 24 - timereset

    # QR CODE
    code = qr_code_reader(frame)
    if code is not None:
        code = code.decode()
        valid = compare_qrcode(code)
        if valid:
            today = datetime.datetime.today()
            datestamp = today.strftime("%m/%d/%Y, %H:%M:%S")
            date = today.strftime("%m-%d-%Y")
            post_log(str(code), "QRcode")
            mode = 'a' if path.isfile("log/" + date) else 'w'
            with open("log/" + date, mode) as log:
                log.write(str(code) + " / QRcode / " + str(datestamp) + "\n")
                log.close()
            if not authorized.is_alive():
                print("ouverture porte")
                authorized = threading.Thread(None, lock_control, None, ("authorized", "invité"), {})
                get_audio("ouverture")
                authorized.start()
        else:
            if not unauthorized.is_alive() and not authorized.is_alive():
                unauthorized = threading.Thread(None, lock_control, None, ("unauthorized", "no"), {})
                unauthorized.start()

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.1)
