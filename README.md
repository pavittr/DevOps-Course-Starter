# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Accessing Trello APIs

The application stores data in a Trello board. To set this up you will need a Trello developer account and a board ID. Follow the steps below to set up Trello access, your API key, and the board you will use to store your items on.

1. To create a developer account visit [https://trello.com/signup] and create a new account. Once signed up you will drop into the Trello dashboard.
2. Create a new board and give it a descriptive name (e.g. `Todo App`).
3. In the browser window append `.json` to the end of the trello url (so [https://trello.com/b/abc123/todoapp] becomes [https://trello.com/b/abc123/todoapp.json])
4. The browser window will display JSON related to the board. At the start will be an `ID` field. Make a note of this as you will need to add it to the `.env` as the `TRELLO_BOARD_ID` environment variable.
5. Add the following two lists to the board:
    * `Not Started`
    * `Completed`
6. Once this is done, navigate to [https://trello.com/app-key] and follow the instructions to create a Developer API Key and a Token.
    * Its worth noting that the API key displays at the start of the page, however as of writing the token needs to be gathered from the a link on the same page that specifies that you need to geenrate a Token.
7. Once you have these details set, update the `.env` file with the following variables:
    * `TRELLO_SERVER_TOKEN` - Token from following the instructions to generate a Token from [https://trello.com/app-key]
    * `TRELLO_API_KEY` - Developer key displayed at [https://trello.com/app-key]
    * `TRELLO_BOARD_ID` - The ID found in the board's JSON output
    * `TRELLO_WORKSPACE_ID` - Boards need to be assigned to a workspace. If you navigate to `https://trello.com` you will be redirected to a URL containing your workspace ID (something like `workspace123456`). Set this variable to that value.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running tests

The app uses `pyest` to run most tests. To get the tests up and running run the following command:

```
poetry run pytest --cov=todo_app
```

As well as running the tests this will also give you coverage info to understand where tests need to be added.

### Integration tests using Selenium

To run the selenium tests Firefox must be installed locally, and the Gecko driver must be on the PATH.

1. Download Firefox from [https://www.mozilla.org/en-GB/firefox/new/](https://www.mozilla.org/en-GB/firefox/new/)
2. Download the Gecko driver from [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases). Extract the driver and ensure it is on your PATH.