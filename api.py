import requests
import json


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


response = requests.get("http://api.open-notify.org/astros.json")
json_res = response.json()

jprint(json_res)
