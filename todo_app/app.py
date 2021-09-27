import json
import os

from flask.wrappers import Response

from todo_app.items.item import ItemEncoder
from todo_app.view_model import ViewModel
from todo_app.items.trello.transport import TrelloTransport
from flask import Flask, render_template, request

from todo_app.items.trello.items import Items



def create_app():
    app = Flask(__name__)
    # We specify the full path and remove the import for this config so
    # it loads the env variables when the app is created, rather than when this file is imported
    app.config.from_object('todo_app.flask_config.Config')

    trello_transport = TrelloTransport(os.environ.get('TRELLO_API_KEY'), 
        os.environ.get('TRELLO_SERVER_TOKEN'))
    item_registry = Items(trello_transport, os.environ.get('TRELLO_BOARD_ID'))

    @app.route('/')
    def index():
        app.logger.info("Request received to load root")
        return render_template('index.html')

    @app.route('/todo')
    def get_all_items():
        items = sorted(item_registry.get_items(), key=lambda item: item.status, reverse=True)
        item_view_model = ViewModel(items)
        status = request.args.get('status')
        switch = {
            "todo": item_view_model.to_do_items,
            "doing": item_view_model.doing_items,
            "done": item_view_model.done_items,
        }

        return json.dumps(sorted(switch.get(status, item_view_model.items), key=lambda item: item.status, reverse=True), cls=ItemEncoder)

    @app.route('/todo/add', methods = ['POST'])
    def create_new_todo():
        title = request.form['title']
        new_item = item_registry.add_item(title)
        return json.dumps(new_item, cls=ItemEncoder)

    @app.route('/todo/<item_id>/status', methods = ['PUT'])
    def change_state(item_id):
        app.logger.info("Form data for %s: %s %s", item_id, request.form, request.get_data(as_text = True))
        new_item = item_registry.save_item({'id':item_id, 'status': request.get_data(as_text = True)})
        return json.dumps(new_item, cls=ItemEncoder)

    @app.route('/todo/<item_id>', methods = ['DELETE'])
    def delete_existing_todo(item_id):
        app.logger.info('Request to delete ID %s', item_id)
        return item_registry.delete_item(item_id)

    @app.route("/healthcheck")
    def healthcheck():
        return Response("{'status':'up'}", status=200, mimetype='application/json')

    return app
