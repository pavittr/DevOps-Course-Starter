import os
from todo_app.items.trello.transport import TrelloTransport
from flask import Flask, render_template, request

from todo_app.flask_config import Config

from todo_app.items.trello.items import Items

app = Flask(__name__)
app.config.from_object(Config)
trello_transport = TrelloTransport(os.environ.get('TRELLO_API_KEY'), 
        os.environ.get('TRELLO_SERVER_TOKEN'))
item_registry = Items(trello_transport, os.environ.get('TRELLO_BOARD_ID'))

@app.route('/')
def index():
    items = sorted(item_registry.get_items(), key=lambda item: item.status, reverse=True)
    return render_template('index.html', items=items)

@app.route('/todo/add', methods = ['POST'])
def create_new_todo():
    title = request.form['title']
    return item_registry.add_item(title).toJSON()

@app.route('/todo/<item_id>/status', methods = ['PUT'])
def change_state(item_id):
    app.logger.info("Form data for %s: %s %s", item_id, request.form, request.get_data(as_text = True))
    return item_registry.save_item({'id':item_id, 'status': request.get_data(as_text = True)}).toJSON()

@app.route('/todo/<item_id>', methods = ['DELETE'])
def delete_existing_todo(item_id):
    app.logger.info('Request to delete ID %s', item_id)
    return item_registry.delete_item(item_id)

if __name__ == '__main__':
    app.run()
