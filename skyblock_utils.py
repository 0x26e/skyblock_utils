import requests
import json
from pprint import pprint

def get_info(call):
    r = requests.get(call)
    return r.json()

API_FILE = open("API_KEY.json", "r")
API_KEY = json.loads(API_FILE.read())["API_KEY"]

pprint(API_KEY)


























#
