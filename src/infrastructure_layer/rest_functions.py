import requests


url = 'http://127.0.0.1'
port = ':3002'


def post(path, message):
    r = requests.request('POST', url+port+path, json=message)
    return r


def put(path, message):
    r = requests.request('PUT', url+port+path, json=message)
    return r


def get(path, message):
    r = requests.request('GET', url+port+path, params=message)
    return r


def delete(path, message):
    r = requests.request('DELETE', url+port+path, json=message)
    return r