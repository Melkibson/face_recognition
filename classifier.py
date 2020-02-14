import face_recognition
import cv2
import numpy as np
import os
from pprint import pprint

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
yamna_image = face_recognition.load_image_file("training-data/yamna/1.JPG")
yamna_face_encoding = face_recognition.face_encodings(yamna_image)[0]

np.savetxt('training-data/yamna/yamna.txt', yamna_face_encoding)
yamna = np.loadtxt('training-data/yamna/yamna.txt')

leo_image = face_recognition.load_image_file("training-data/leo/1.jpg")
leo_face_encoding = face_recognition.face_encodings(leo_image)[0]

mathias_image = face_recognition.load_image_file("training-data/mathias/1.jpg")
mathias_face_encoding = face_recognition.face_encodings(mathias_image)[0]

paul_image = face_recognition.load_image_file("training-data/paul/1.jpg")
paul_face_encoding = face_recognition.face_encodings(paul_image)[0]

ahmed_image = face_recognition.load_image_file("training-data/ahmed/1.jpg")
ahmed_face_encoding = face_recognition.face_encodings(ahmed_image)[0]

jonathan_image = face_recognition.load_image_file("training-data/jon/1.jpg")
jonathan_face_encoding = face_recognition.face_encodings(jonathan_image)[0]

camille_image = face_recognition.load_image_file("training-data/camille/1.jpg")
camille_face_encoding = face_recognition.face_encodings(camille_image)[0]

dorian_image = face_recognition.load_image_file("training-data/dorian/1.jpg")
dorian_face_encoding = face_recognition.face_encodings(dorian_image)[0]

nico_image = face_recognition.load_image_file("training-data/niko/1.jpg")
nico_face_encoding = face_recognition.face_encodings(nico_image)[0]

tchoupi_image = face_recognition.load_image_file("training-data/tchoupi/1.jpg")
tchoupi_face_encoding = face_recognition.face_encodings(tchoupi_image)[0]

fred_image = face_recognition.load_image_file("training-data/fred/1.jpg")
fred_face_encoding = face_recognition.face_encodings(fred_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    yamna,
    leo_face_encoding,
    mathias_face_encoding,
    paul_face_encoding,
    ahmed_face_encoding,
    jonathan_face_encoding,
    camille_face_encoding,
    dorian_face_encoding,
    nico_face_encoding,
    tchoupi_face_encoding,
    fred_face_encoding

]
known_face_names = [
    "Melkibson",
    "Novaedra",
    "MaTHC",
    "DarkPaul18",
    "Ben Benzema",
    "Kanarpp",
    "Cynath17",
    "Dodo le dozo",
    "Niko le Proprio",
    "Tchoupi en colere",
    "Frederic Noel"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

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

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
