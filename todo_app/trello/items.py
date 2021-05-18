import requests
import os
    
def get_lists():
    BOARD_ID = os.environ.get('BOARD_ID')
    r = call_trello('GET', f"/1/boards/{BOARD_ID}/lists")
    return list(map(lambda list: {'id': list['id'], 'name': list['name']}, r.json()))

def get_list_by_name(list_name, list_map):
    return next(filter(lambda list: list['name'] == list_name, list_map))
    
def convert_trello_to_todo(trello_card, list_map):
    list_by_id = next(filter(lambda list: list['id'] == trello_card['idList'], list_map))
    return {'id': trello_card['id'], 'title': trello_card['name'], 'status': list_by_id['name']}

def call_trello(method, path, payload={}):
    payload['key'] = os.environ.get('TRELLO_API_KEY')
    payload['token'] = os.environ.get('TRELLO_SERVER_TOKEN')
    return requests.request(method, f"https://api.trello.com{path}", params=payload)

def get_items():
    """
    Fetches cards from Trello
    """
    lists = list(filter(lambda list: list['name'] in ['Not Started', 'Completed'], get_lists()))
    cards = []
    for req_list in lists:
        r = call_trello('GET', f"/1/lists/{req_list['id']}/cards")
        cards = cards + list(map(lambda card : {'id': card['id'], 'title': card['name'], 'status': req_list['name']}, r.json()))
    return cards

def add_item(title):
    """
    Add a new card to the board. Cards are assumed to start in the Not Started state

    Args:
        item: The item to create.
    """
    lists = get_lists()
    todoList = get_list_by_name('Not Started', lists)
    r = call_trello('POST', '/1/cards', {'idList': todoList['id'], 'name': title})
    return convert_trello_to_todo(r.json(), lists)

def save_item(item):
    """
    Updates an existing item. At present only changes to
    the Status (i.e. the list the card is associated with) are stored

    Args:
        item: The item to save.
    """
    lists = get_lists()
    expectedList = get_list_by_name(item['status'], lists)
    r = call_trello('PUT', f"/1/cards/{item['id']}", {'idList': expectedList['id']})
    return convert_trello_to_todo(r.json(), lists)

def delete_item(item_id):
    """
    Deletes an existing item. Attempted to delete a card that doesn't exist is undefined.

    Args:
        item_id: The item to delete.
    """
    r = call_trello('DELETE', f"/1/cards/{item_id}")
    return  {}