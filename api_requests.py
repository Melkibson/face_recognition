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


def compare_qrcode(code):
    headers = authenticate()
    session = get_session()
    url_qrcode = getenv('API_QRCODE_ROUTE') + str(code)

    with session.get(url_qrcode, headers=headers) as response:
        if response:
            print('code:' + loads(response.text)['qrcode'])
        else:
            print('wrong code')


# def post_audio(sound):
#     headers = authenticate()
#     session = get_session()
#     url_audio = getenv('API_AUDIO_ROUTE')
#     with session.post(url_audio, headers=headers) as response:
#         return response.text











