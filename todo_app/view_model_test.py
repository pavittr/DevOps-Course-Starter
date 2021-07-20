from todo_app.view_model import ViewModel
from todo_app.items.item import Item
import pytest


def test_items_property():
    items = [Item("id1", "title1", "To Do"), Item("id2", "title2", "Doing"), Item("id3", "title3", "Done")]

    view_model = ViewModel(items)

    all_items = view_model.items

    assert len(all_items) == 3

    todo_item_1 = all_items[0]

    assert todo_item_1.id == "id1"
    assert todo_item_1.title == "title1"
    assert todo_item_1.status == "To Do"

    doing_item_1 = all_items[1]

    assert doing_item_1.id == "id2"
    assert doing_item_1.title == "title2"
    assert doing_item_1.status == "Doing"

    done_item_1 = all_items[2]

    assert done_item_1.id == "id3"
    assert done_item_1.title == "title3"
    assert done_item_1.status == "Done"



def test_filtering_items():
    items = [Item("id1", "title1", "To Do"), Item("id2", "title2", "Done")]

    view_model = ViewModel(items)

    todo_items = view_model.get_items(["To Do"])

    assert len(todo_items) == 1

    todo_item = todo_items[0]

    assert todo_item.id == "id1"
    assert todo_item.title == "title1"
    assert todo_item.status == "To Do"


def test_get_items_filters_out_other_types():
    items = [Item("id1", "title1", "To Do"), Item("id2", "title2", "Doing"), Item("id3", "title3", "Done")]

    view_model = ViewModel(items)

    todo_items = view_model.get_items(["Doing"])

    assert len(todo_items) == 1

    todo_item_1 = todo_items[0]

    assert todo_item_1.id == "id2"
    assert todo_item_1.title == "title2"
    assert todo_item_1.status == "Doing"


def test_no_filter():
    items = [Item("id1", "title1", "To Do"), Item("id2", "title2", "Done")]

    view_model = ViewModel(items)

    todo_items = view_model.get_items()

    assert len(todo_items) == 0


def test_to_do_items_property():
    items = [Item("id1", "title1", "To Do"), Item("id2", "title2", "Doing"), Item("id3", "title3", "Done")]

    view_model = ViewModel(items)

    todo_items = view_model.to_do_items

    assert len(todo_items) == 1

    todo_item_1 = todo_items[0]

    assert todo_item_1.id == "id1"
    assert todo_item_1.title == "title1"
    assert todo_item_1.status == "To Do"

def test_doing_items_property():
    items = [Item("id1", "title1", "To Do"), Item("id2", "title2", "Doing"), Item("id3", "title3", "Done")]

    view_model = ViewModel(items)

    doing_items = view_model.doing_items

    assert len(doing_items) == 1

    doing_item_1 = doing_items[0]

    assert doing_item_1.id == "id2"
    assert doing_item_1.title == "title2"
    assert doing_item_1.status == "Doing"


def test_done_items_property():
    items = [Item("id1", "title1", "To Do"), Item("id2", "title2", "Doing"), Item("id3", "title3", "Done")]

    view_model = ViewModel(items)

    done_items = view_model.done_items

    assert len(done_items) == 1

    done_item_1 = done_items[0]

    assert done_item_1.id == "id3"
    assert done_item_1.title == "title3"
    assert done_item_1.status == "Done"