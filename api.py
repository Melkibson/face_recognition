import concurrent.futures
import requests
import threading
import os
import json
import time

thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def authenticate():
    url_login = os.getenv('API_LOGIN_ROUTE')
    params = {"email": "yam@yam.fr", "password": "yam"}
    session = get_session()
    with session.post(url_login, params) as response:
        token = json.loads(response.text)['token']
    response = requests.post(url_login, params)
    token = json.loads(response.text)['token']

    headers = {
        "Authorization": "Bearer " + token,
        "content-type": "application/json",
    }