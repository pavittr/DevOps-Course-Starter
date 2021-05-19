from flask import Flask, render_template, request

from todo_app.flask_config import Config

from todo_app.items.trello.items import add_item, delete_item, get_items, save_item

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    items = sorted(get_items(), key=lambda item: item.status, reverse=True)
    return render_template('index.html', items=items)

@app.route('/todo/add', methods = ['POST'])
def create_new_todo():
    title = request.form['title']
    return add_item(title).toJSON()

@app.route('/todo/<item_id>/status', methods = ['PUT'])
def change_state(item_id):
    app.logger.info("Form data for %s: %s %s", item_id, request.form, request.get_data(as_text = True))
    return save_item({'id':item_id, 'status': request.get_data(as_text = True)}).toJSON()

@app.route('/todo/<item_id>', methods = ['DELETE'])
def delete_existing_todo(item_id):
    app.logger.info('Request to delete ID %s', item_id)
    return delete_item(item_id)

if __name__ == '__main__':
    app.run()
