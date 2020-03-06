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


def returnLog(pseudo, method):
    headers = authenticate()
    session = get_session()
    url_log = getenv('API_LOG_ROUTE')

    # data to be sent to api
    data = {
        "pseudo":pseudo,
        "method":method
    }

    with session.post("http://kanarpp.xyz:3000/log", headers=headers, data=data) as response:
        if response:
            token = loads(response.text)['log']
        else:
            print("error")
        return response
