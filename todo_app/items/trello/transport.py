import requests
import os

def call_trello(method, path, payload={}):
    payload['key'] = os.environ.get('TRELLO_API_KEY')
    payload['token'] = os.environ.get('TRELLO_SERVER_TOKEN')
    return requests.request(method, f"https://api.trello.com{path}", params=payload)