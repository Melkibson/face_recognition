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
            "Authorization": "Bearer " + token,
            "content-type": "application/json",
        }
        return headers


headers = authenticate()


def get_users():
    url_users = getenv('API_ALL_USERS_ROUTE')
    with session.get(url_users, headers=headers) as response:
        all_users = loads(response.text)['data']
        return all_users


def get_user_by_id():
    length = len(get_users())
    for i in range(length):
        url_user = getenv('API_USER_ROUTE')
        _id = get_users()[i]['_id']
        with session.get(url_user % _id, headers=headers) as response:
            user_data = loads(response.text)['data']
    return user_data


def compare_qrcode(code):
    url_qrcode = getenv('API_QRCODE_ROUTE') + str(code)

    with session.get(url_qrcode, headers=headers) as response:
        if response:
            print('code:' + loads(response.text)['qrcode'])
        else:
            print('wrong code')


def get_audio():
    _id = get_user_by_id()['_id']
    url_audio = getenv('API_AUDIO_ROUTE')
    with session.get(url_audio % _id, headers=headers) as response:
        link = 'defaut.mp3'
        if link is not 'defaut.mp3':
            link = 'http://' + loads(response.text)['link']
            sound = vlc.MediaPlayer(link)
            return sound.play()
        else:
            sound = vlc.MediaPlayer(link)
            return sound.play()


def get_user_img():
    _id = get_user_by_id()['_id']
    url_img = getenv('API_USER_IMG_ROUTE')
    with session.post(url_img % _id, headers=headers) as response:
        print(loads(response.text))


print(get_user_img())


