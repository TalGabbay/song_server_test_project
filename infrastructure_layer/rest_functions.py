import requests
import os
from project_definitions import ROOT_DIR
from configparser import ConfigParser

file = os.path.join(ROOT_DIR, "config.ini")
config = ConfigParser()
config.read(file)

url = config["server_info"]["url"]
port = config["server_info"]["port"]
host = "http://"+url+":"+port


print(config["server_info"]["url"])


def post(path, message):
    r = requests.request('POST', host+path, json=message)
    return r


def put(path, message):
    r = requests.request('PUT', host+path, json=message)
    return r


def get(path, message):
    r = requests.request('GET', host+path, params=message)
    return r


def delete(path, message):
    r = requests.request('DELETE', host+path, json=message)
    return r