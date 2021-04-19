from flask import Flask, render_template, request

from todo_app.flask_config import Config

from todo_app.data.session_items import add_item, get_items

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items = get_items()
    return render_template('index.html', items=items)

@app.route('/todo/add', methods = ['POST'])
def create_new_todo():
    title = request.form['title']
    return add_item(title)

if __name__ == '__main__':
    app.run()
