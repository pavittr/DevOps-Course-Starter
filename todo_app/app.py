from flask import Flask, render_template, request

from todo_app.flask_config import Config

from todo_app.data.session_items import add_item, delete_item, get_items, save_item

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items = sorted(get_items(), key=lambda item: item['status'], reverse=True)
    return render_template('index.html', items=items)

@app.route('/todo/add', methods = ['POST'])
def create_new_todo():
    title = request.form['title']
    return add_item(title)

@app.route('/todo/<itemId>/status', methods = ['PUT'])
def change_state(itemId):
    item = list(filter(lambda item: item['id'] == int(itemId), get_items())).pop()
    app.logger.info("Form data %s %s", request.form, request.get_data(as_text = True))
    item['status'] = request.get_data(as_text = True)
    app.logger.info("Request to update Item %s: %s", itemId, item)
    return save_item(item)

@app.route('/todo/<itemId>', methods = ['DELETE'])
def delete_existing_todo(itemId):
    app.logger.info('Request to delete ID %s', itemId)
    return delete_item(int(itemId))

if __name__ == '__main__':
    app.run()
