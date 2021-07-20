import json
from dotenv.main import find_dotenv, load_dotenv
from unittest.mock import Mock, patch
from todo_app import app
import pytest

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = app.create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

@patch('requests.request')
def test_todo_url(mock_request_requests, client):
    # Replace call to requests.requests(method, url) with our own function
    mock_request_requests.side_effect = mock_make_request
    response = client.get('/todo')
    data = json.JSONDecoder().decode(response.data.decode("utf-8") )
    assert len(data) == 9
    assert number_of_todos_with_status('To Do', data) == 3
    assert number_of_todos_with_status('Doing', data) == 3
    assert number_of_todos_with_status('Done', data) == 3

    assert number_of_todos_with_title('To Do Item 1', data) == 1
    assert number_of_todos_with_title('To Do Item 2', data) == 1
    assert number_of_todos_with_title('To Do Item 3', data) == 1
    assert number_of_todos_with_title('Doing Item 1', data) == 1
    assert number_of_todos_with_title('Doing Item 2', data) == 1
    assert number_of_todos_with_title('Doing Item 3', data) == 1
    assert number_of_todos_with_title('Done Item 1', data) == 1
    assert number_of_todos_with_title('Done Item 2', data) == 1
    assert number_of_todos_with_title('Done Item 3', data) == 1

def number_of_todos_with_status(status, todos):
    return len(list(filter(lambda todo: todo['status'] == status, todos)))

def number_of_todos_with_title(title, todos):
    return len(list(filter(lambda todo: todo['title'] == title, todos)))



def mock_make_request(method, url, params):
    if url == f'https://api.trello.com/1/boards/FAKE_BOARD_ID/lists':
        response = Mock()
        # sample_trello_lists_response should point to some test response data
        response.json.return_value = [
            {'id': "todo_list_id", 'name': "To Do"},
            {'id': "doing_list_id", 'name': "Doing"},
            {'id': "done_list_id", 'name': "Done"}]
        return response
    elif url == f'https://api.trello.com/1/lists/todo_list_id/cards':
        response = Mock()
        response.json.return_value = [
            {'id': "todo_item_1", 'name': "To Do Item 1", 'idList' : 'todo_list_id'},
            {'id': "todo_item_2", 'name': "To Do Item 2", 'idList' : 'todo_list_id'},
            {'id': "todo_item_3", 'name': "To Do Item 3", 'idList' : 'todo_list_id'}]
        return response
    elif url == f'https://api.trello.com/1/lists/doing_list_id/cards':
        response = Mock()
        response.json.return_value = [
            {'id': "doing_item_1", 'name': "Doing Item 1", 'idList' : 'doing_list_id'},
            {'id': "doing_item_2", 'name': "Doing Item 2", 'idList' : 'doing_list_id'},
            {'id': "doing_item_3", 'name': "Doing Item 3", 'idList' : 'doing_list_id'}]
        return response
    elif url == f'https://api.trello.com/1/lists/done_list_id/cards':
        response = Mock()
        response.json.return_value = [
            {'id': "done_item_1", 'name': "Done Item 1", 'idList' : 'done_list_id'},
            {'id': "done_item_2", 'name': "Done Item 2", 'idList' : 'done_list_id'},
            {'id': "done_item_3", 'name': "Done Item 3", 'idList' : 'done_list_id'}]
        return response
    return None