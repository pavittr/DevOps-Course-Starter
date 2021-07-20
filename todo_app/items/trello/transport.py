import requests
import os

class TrelloTransport:

    def __init__(self, trello_api, trello_server_token) -> None:
        self.trello_api = trello_api
        self.trello_server_token = trello_server_token

    def call_trello(self, method, path, payload={}):
        payload['key'] = self.trello_api
        payload['token'] = self.trello_server_token
        return requests.request(method, f"https://api.trello.com{path}", params=payload)