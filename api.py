import concurrent.futures
import requests
import threading
import json


thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def get_login():
    session = get_session()
    params = {"email": "yam@yam.fr", "password": "yam"}
    url_login = 'http://kanarpp.xyz:3000/user/login'
    url_qrcode = 'http://kanarpp.xyz:3000/qrcode'
    with session.post(url_login, data=params) as response:
        token = json.loads(response.text)['token']
        headers = {
            "Authorization": "Bearer " + token,
            "content-type": "application/json",
        }
        with session.get(url_qrcode, headers=headers) as res:

            user_codes = json.loads(res.text)
            for user_code in user_codes['data']:
                qr_code = user_code['qrcode']
                print(qr_code)


if __name__ == '__main__':
    get_login()
