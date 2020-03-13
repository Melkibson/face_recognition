import requests
from os import getenv
from dotenv import load_dotenv
from json import loads
import vlc

env = load_dotenv('.env')
session = requests.Session()


def authenticate():
    params = {"email": getenv('EMAIL'), "password": getenv('PASSWORD')}
    url_login = getenv('API_LOGIN_ROUTE')
    with session.post(url_login, data=params) as response:
        token = loads(response.text)['token']
        headers = {
            "Authorization": "Bearer " + token
        }
        return headers


def get_users():
    headers = authenticate()
    url_users = getenv('API_ALL_USERS_ROUTE')
    with session.get(url_users, headers=headers) as response:
        all_users = loads(response.text)['data']
        return all_users


def get_user_by_id():
    headers = authenticate()
    length = len(get_users())
    for i in range(length):
        _id = get_users()[i]['_id']
        url_user = getenv('API_USER_ROUTE') + str(_id)
        with session.get(url_user, headers=headers) as response:
            user_data = loads(response.text)['data']
    return user_data


def compare_qrcode(code):
    headers = authenticate()
    url_qrcode = getenv('API_QRCODE_ROUTE') + str(code)

    with session.get(url_qrcode, headers=headers) as response:
        if response:
            return True
        else:
            return False


def get_audio(status):
    headers = authenticate()
    # id = get_user_by_id()['_id']
    _id = "5e6a14e43a2b8f4550db02c4"
    url_audio = getenv('API_AUDIO_ROUTE') + str(_id)
    if status == "ouverture":
        with session.get(url_audio, headers=headers) as response:
            link = 'defaut.mp3'
            if link is not 'defaut.mp3':
                link = 'http://' + loads(response.text)['link']
                sound = vlc.MediaPlayer(link)
                return sound.play()
            else:
                sound = vlc.MediaPlayer(link)
                return sound.play()
    else:
        sound = vlc.MediaPlayer("fermeture.mp3")
        return sound.play()


def post_log(name, method):
    headers = authenticate()
    url_log = getenv('API_LOG_ROUTE')
    mydata = {"pseudo": name, "method": method}
    with session.post(url_log, headers=headers, data=mydata) as response:
        print(response.text)
