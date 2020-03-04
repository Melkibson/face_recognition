import requests
import threading
from json import loads


thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def authenticate():
    session = get_session()
    params = {"email": "yam@yam.fr", "password": "yam"}
    url_login = 'http://kanarpp.xyz:3000/user/login'
    with session.post(url_login, data=params) as response:
        token = loads(response.text)['token']
        headers = {
            "Authorization": "Bearer " + token,
            "content-type": "application/json",
        }
        return headers


def get_qrcode():
    headers = authenticate()
    session = get_session()
    url_qrcode = 'http://kanarpp.xyz:3000/qrcode'
    with session.get(url_qrcode, headers=headers) as response:

        user_codes = loads(response.text)
        for user_code in user_codes['data']:
            qr_code = user_code['qrcode']
            return qr_code




