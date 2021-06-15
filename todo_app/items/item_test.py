from todo_app.items.item import Item, ItemEncoder

import pytest, json

def test_JSON_encoder_returns_correct_fields():
    item = Item("ID", "TITLE", "STATUS")
    item_json  = json.dumps(item, cls=ItemEncoder)
    single_element = json.loads(item_json)
    assert single_element['id'] == "ID"
    assert single_element['title'] == "TITLE"
    assert single_element['status'] == "STATUS"

def test_JSON_encoder_returns_correct_fields_for_multiple_items():
    items = [Item("ID2", "TITLE2", "STATUS2"), Item("ID3", "TITLE3", "STATUS3"), Item("ID1", "TITLE1", "STATUS1")]
    # Note the sort here to make testing a little eeasier
    item_json  = json.dumps(sorted(items, key=lambda item: item.status, reverse=True), cls=ItemEncoder)
    json_dict = json.loads(item_json)
    assert len(json_dict) == 3
    item_1 = json_dict[0]
    assert item_1['id'] == "ID3"
    assert item_1['title'] == "TITLE3"
    assert item_1['status'] == "STATUS3"  
    item_2 = json_dict[1]  
    assert item_2['id'] == "ID2"
    assert item_2['title'] == "TITLE2"
    assert item_2['status'] == "STATUS2"   
    item_3 = json_dict[2] 
    assert item_3['id'] == "ID1"
    assert item_3['title'] == "TITLE1"
    assert item_3['status'] == "STATUS1"    