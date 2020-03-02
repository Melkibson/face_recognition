import cv2
import pyzbar.pyzbar as pyzbar
import requests
import json


def qr_code_reader(code):
    camera = cv2.VideoCapture(0)
    capture = True
    while capture:
        ret, frame = camera.read()
        decodedObjects = pyzbar.decode(frame)
        for obj in decodedObjects:
            decoded = decodedObjects[0].data
            if decoded == bytes(code, 'utf-8'):
                print("Access granted")
            else:
                print("Access denied")

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


video_capture = cv2.VideoCapture(0)

url_login = 'http://kanarpp.xyz:3000/user/login'
url_qrcode = 'http://kanarpp.xyz:3000/qrcode'

params = {"email": "yam@yam.fr", "password": "yam"}


response = requests.post(url_login, params)
token = json.loads(response.text)['token']

headers = {
    "Authorization": "Bearer " + token,
    "content-type": "application/json",
}
try:
    response = requests.get(url_qrcode, headers=headers)
    user_codes = json.loads(response.text)
    for user_code in user_codes['data']:
        qr_code = user_code['qrcode']
        qr_code_reader(qr_code)
except requests.exceptions.ConnectionError:
    response.status_code = "Connection refused"


