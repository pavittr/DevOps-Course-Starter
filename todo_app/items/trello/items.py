import os
from todo_app.items.item  import Item
from todo_app.items.trello.list import List

class Items:
    def __init__(self, trello_transport, board_id) -> None:
        self.trello_transport = trello_transport
        self.board_id = board_id

    def item_from_trello(trello_json, list_map):
        """
        Converts a JSON object representing a Trello card into a Todo Item.
        """
        list_by_id = next(filter(lambda list: list.id == trello_json['idList'], list_map))
        return Item(trello_json['id'], trello_json['name'], list_by_id.name)

    def get_lists(self):
        """
        Inspects the specified board and finds all lists for that particular board.
        Board ID is fixed at run time and cannot be changed by users
        """
        r = self.trello_transport.call_trello('GET', f"/1/boards/{self.board_id}/lists")
        return list(map(lambda list_json: List.fromJson(list_json), r.json()))

    def get_list_by_name(list_name, list_map):
        """
        Simple filter to look up a list object using the name of the list
        """
        return next(filter(lambda list: list.name == list_name, list_map))

    def get_items(self):
        """
        Fetches cards from Trello
        """
        lists = list(filter(lambda list: list.name in ['Not Started', 'Completed'], self.get_lists()))
        cards = []
        for req_list in lists:
            r = self.trello_transport.call_trello('GET', f"/1/lists/{req_list.id}/cards")
            cards = cards + list(map(lambda card : Items.item_from_trello(card, lists), r.json()))
        return cards

    def add_item(self, title):
        """
        Add a new card to the board. Cards are assumed to start in the Not Started state

        Args:
            item: The item to create.
        """
        lists = self.get_lists()
        todoList = Items.get_list_by_name('Not Started', lists)
        r = self.trello_transport.call_trello('POST', '/1/cards', {'idList': todoList.id, 'name': title})
        return Items.item_from_trello(r.json(), lists)

    def save_item(self, item):
        """
        Updates an existing item. At present only changes to
        the Status (i.e. the list the card is associated with) are stored

        Args:
            item: The item to save.
        """
        lists = self.get_lists()
        expectedList = Items.get_list_by_name(item['status'], lists)
        r = self.trello_transport.call_trello('PUT', f"/1/cards/{item['id']}", {'idList': expectedList.id})
        return Items.item_from_trello(r.json(), lists)

    def delete_item(self, item_id):
        """
        Deletes an existing item. Attempted to delete a card that doesn't exist is undefined.

        Args:
            item_id: The item to delete.
        """
        r = self.trello_transport.call_trello('DELETE', f"/1/cards/{item_id}")
        return  {}