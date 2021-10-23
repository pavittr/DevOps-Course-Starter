import os
from threading import Thread

import pytest
import requests
from dotenv.main import find_dotenv, load_dotenv
from requests.adapters import ConnectionError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from todo_app import app
from todo_app.items.trello.boards import Boards
from todo_app.items.trello.transport import TrelloTransport

def wait_for_up():
    retries = 10
    counter = 1
    working = False
    while not working and counter <= retries:
        counter = counter + 1
        try:
            response = requests.get("http://localhost:5000/healthcheck", timeout=(30, 5))
            if response.status_code == 200:
                working = True
        except ConnectionError:
            pass

def get_board():
    file_path = find_dotenv(usecwd=True)
    load_dotenv(file_path, override=True)
    # Create the new board & update the board id environment variable
    trello_transport = TrelloTransport(os.environ.get('TRELLO_API_KEY'), os.environ.get('TRELLO_SERVER_TOKEN'))
    return Boards(trello_transport)

@pytest.fixture(scope='module')
def app_with_temp_board():
    boards = get_board()
    board_id = boards.create_trello_board(os.environ.get('TRELLO_WORKSPACE_ID'))
    os.environ['TRELLO_BOARD_ID'] = board_id
    # construct the new application
    application = app.create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    wait_for_up()
    yield application
    # Tear Down
    thread.join(1)
    boards.delete_trello_board(board_id)

@pytest.fixture
def driver(request):
    if request.param == 'chrome_driver':
        opts = webdriver.ChromeOptions()
        opts.add_argument('--headless')
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        with webdriver.Chrome(options=opts) as driver:
            yield driver
    elif request.param == 'firefox_driver':
        with webdriver.Firefox() as driver:
            yield driver
    else:
        raise ValueError("unrecognised driver " + request.param)

@pytest.mark.parametrize('driver', ['chrome_driver', 'firefox_driver'], indirect=True)
def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

    new_item_text_box = driver.find_element_by_id("new_item_title")
    new_item_text_box.send_keys("test object")
    new_item_text_box.send_keys(Keys.RETURN)
    todo_list = driver.find_element_by_id("todo_list")
    new_item_list_item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "li"))
    )
    title_of_item = new_item_list_item.find_element_by_tag_name("a")
    assert title_of_item.get_attribute('innerHTML') == "test object"
