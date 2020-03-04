import requests
from threading import local
from os import getenv
from dotenv import load_dotenv
from json import loads


thread_local = local()
env = load_dotenv('.env')


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def authenticate():
    session = get_session()
    params = {"email": getenv('EMAIL'), "password": getenv('PASSWORD')}
    url_login = getenv('API_LOGIN_ROUTE')
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
    url_qrcode = getenv('API_QRCODE_ROUTE')
    with session.get(url_qrcode, headers=headers) as response:

        user_codes = loads(response.text)
        for user_code in user_codes['data']:
            qr_code = user_code['qrcode']
            return qr_code






