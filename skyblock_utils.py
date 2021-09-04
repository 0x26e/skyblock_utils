# Imports
import requests
import json
from pprint import pprint

# Functions
def get_info(call):
    r = requests.get(call)
    return r.json()

# Variables
API_FILE = open("API_KEY.json", "r")
API_KEY = json.loads(API_FILE.read())["API_KEY"]


# Code
