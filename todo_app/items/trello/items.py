import os
from todo_app.items.item  import Item
from todo_app.items.trello.list import List
from todo_app.items.trello.transport import call_trello

def item_from_trello(trello_json, list_map):
    """
    Converts a JSON object representing a Trello card into a Todo Item.
    """
    list_by_id = next(filter(lambda list: list.id == trello_json['idList'], list_map))
    return Item(trello_json['id'], trello_json['name'], list_by_id.name)

def get_lists():
    """
    Inspects the specified board and finds all lists for that particular board.
    Board ID is fixed at run time and cannot be changed by users
    """
    TRELLO_BOARD_ID = os.environ.get('TRELLO_BOARD_ID')
    r = call_trello('GET', f"/1/boards/{TRELLO_BOARD_ID}/lists")
    return list(map(lambda list_json: List.fromJson(list_json), r.json()))

def get_list_by_name(list_name, list_map):
    """
    Simple filter to look up a list object using the name of the list
    """
    return next(filter(lambda list: list.name == list_name, list_map))

def get_items():
    """
    Fetches cards from Trello
    """
    lists = list(filter(lambda list: list.name in ['Not Started', 'Completed'], get_lists()))
    cards = []
    for req_list in lists:
        r = call_trello('GET', f"/1/lists/{req_list.id}/cards")
        cards = cards + list(map(lambda card : item_from_trello(card, lists), r.json()))
    return cards

def add_item(title):
    """
    Add a new card to the board. Cards are assumed to start in the Not Started state

    Args:
        item: The item to create.
    """
    lists = get_lists()
    todoList = get_list_by_name('Not Started', lists)
    r = call_trello('POST', '/1/cards', {'idList': todoList.id, 'name': title})
    return item_from_trello(r.json(), lists)

def save_item(item):
    """
    Updates an existing item. At present only changes to
    the Status (i.e. the list the card is associated with) are stored

    Args:
        item: The item to save.
    """
    lists = get_lists()
    expectedList = get_list_by_name(item['status'], lists)
    r = call_trello('PUT', f"/1/cards/{item['id']}", {'idList': expectedList.id})
    return item_from_trello(r.json(), lists)

def delete_item(item_id):
    """
    Deletes an existing item. Attempted to delete a card that doesn't exist is undefined.

    Args:
        item_id: The item to delete.
    """
    r = call_trello('DELETE', f"/1/cards/{item_id}")
    return  {}