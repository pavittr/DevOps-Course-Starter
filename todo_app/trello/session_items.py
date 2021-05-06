import requests
import os

def get_cards_in_list(required_list_name):
    requiredList = get_list(required_list_name)
    r = ask_trello('GET', f"/1/lists/{requiredList['id']}/cards")
    return list(map(lambda card : {'id': card['id'], 'title': card['name'], 'status': requiredList['name']}, r.json()))
    
def get_list(list_name):
    BOARD_ID = os.environ.get('BOARD_ID')
    r = ask_trello('GET', f"/1/boards/{BOARD_ID}/lists")
    lists = list(map(lambda list: {'id': list['id'], 'name': list['name']}, r.json()))
    return next(filter(lambda list: list['name'] == list_name, lists))
    
def ask_trello(method, path, payload={}):
    payload['key'] = os.environ.get('TRELLO_API_KEY')
    payload['token'] = os.environ.get('TRELLO_SERVER_TOKEN')
    return requests.request(method, f"https://api.trello.com{path}", params=payload)

def get_items():
    """
    Fetches cards from Trello
    """
    todoCards = get_cards_in_list('Not Started')
    completedCards = get_cards_in_list('Completed')

    return todoCards + completedCards

def add_item(title):
    """
    Find the lists on the board
    Find the ToDo list and get its cards
    Then find the Done list and get its cards
    """
    todoList = get_list('Not Started')
    r = ask_trello('POST', '/1/cards', {'idList': todoList['id'], 'name': title})
    card = r.json()
    return {'id':card['id'], 'title' : card['name'], 'status': todoList['name']}


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    expectedList = get_list(item['status'])
    ask_trello('PUT', f"/1/cards/{item['id']}", {'idList': expectedList['id']})
    return item

def delete_item(item_id):
    """
    Deletes an existing item in the session. If no existing item matches the ID of the specified item, nothing is deleted.

    Args:
        item_id: The item to delete.
    """
    ask_trello('DELETE', f"/1/cards/{item_id}")
    return  {}
