import requests


url = 'http://127.0.0.1'
port = '3002'
host = url+":"+port


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