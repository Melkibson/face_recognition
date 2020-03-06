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

def returnLog(pseudo, method, datetime):
    header = authenticate()
    session = get_session()

    API_ENDPOINT = "http://kanarpp.xyz:/log"

    # your API key here
    API_KEY = "keyRaspb"

    # your source code here
    log = {
        "pseudo":pseudo,
        "method":method,
        "datetime":datetime
    }

    # data to be sent to api
    data = {'api_dev_key': API_KEY,
            'api_option': 'paste',
            'api_paste_code': log,
            'api_paste_format': 'python'}

    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, data=data)

    # extracting response text
    pastebin_url = r.text
    print("The pastebin URL is:%s" % pastebin_url)
