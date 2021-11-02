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
    * Its worth noting that the API key displays at the start of the page, however as of writing the token needs to be gathered from the a link on the same page that specifies that you need to generate a Token.
7. Once you have these details set, update the `.env` file with the following variables:
    * `TRELLO_SERVER_TOKEN` - Token from following the instructions to generate a Token from [https://trello.com/app-key]
    * `TRELLO_API_KEY` - Developer key displayed at [https://trello.com/app-key]
    * `TRELLO_BOARD_ID` - The ID found in the board's JSON output
    * `TRELLO_WORKSPACE_ID` - Boards need to be assigned to a workspace. If you navigate to `https://trello.com` you will be redirected to a URL containing your workspace ID (something like `workspace123456`). Set this variable to that value.

## Running the App directly

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

## Using Docker

The application is designed to be runnable in Docker as both a development and production version.

### Docker in Development 

The docker image can be built using the following command from the root of the project:

```
docker build  --target development --tag todo-app:dev .
```

This can be followed by running the app with:

```
docker run --env-file ./.env -p 5000:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo-app:dev
```

Note that the app can now be requested by navigating to http://localhst:5000. The files on the local filesystem will be used to run the app, so any changes made will be reflected inside the container just as they are int he non-docker verison.

### Docker in Production

To build the production image, run the following command:

```
docker build --target production --tag todo-app:prod .
```

This can then be deployed with the following command:

```
docker run --env-file ./.env -p 8000:8000 todo-app:prod
```

Note that this time the files cannot be changed from outside the container. To request this version, navigate to http://localhost:8000 in  a browser.


### Running in the background

By default both dev and prod versions will launch in the foreground and so block use of the terminal. If you would like to detach from the process instead, you can use the -d flag to detach from the shell that launches the container. If you wish to view the container logs, you'll need to find the container name (printed by the run command) and then run the following command:

```
docker logs <CONTAINER_NAME>
```

## Running tests

The tests are broken into two sections. These are the unit tests (part of the application) and end to end tests which provide a higher level test flow but require communication to a Trello board.

To run just the unit tests, issue the following command from the root of the project:

```
poetry run pytest --cov=todo_app todo_app
```

As well as running the tests this will also give you coverage info to understand where tests need to be added.

### End to end tests using Selenium

The end to end tests use both Firefox and Chrome, and connect to the Trello backend to create a test board and then manipulate it. In order to get these working you will need to ensure you have both browsers installed as well as the corresponding Selenium drivers. Follow the instructions below to do this.

1. Make sure you have valid Trello credentials in your .env file as listed above (i.e. TRELLO_SERVER_TOKEN and TRELLO_API_KEY).
2. Download Firefox from [https://www.mozilla.org/en-GB/firefox/new/](https://www.mozilla.org/en-GB/firefox/new/)
3. Download the Gecko driver from [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases). Extract the driver and ensure it is on your PATH.
4. Check which version of Chrome you have installed (go to `chrome://settings/help` in the browser and look for the Version string)
5. Go to [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads) and select the driver relating to the OS and Chrome version you are using. Again, ensure this is extracted to somewhere on your PATH.

To run the tests after following these steps, issue the following command:

```
poetry run pytest tests_e2e
```

### Testing in docker

Both sets of tests can be run from inside a docker container. To build the docker test container issue the following command:

```
docker build --target test --tag my-test-image .
```

Once this is built, to run the unit tests run the following command:

```
docker run --env-file=.env.test my-test-image todo_app
```

To run the end to end tests, issue the following command:

```
docker run --env-file=.env my-test-image tests_e2e
```

Note the primary difference between the two types of test here is that whilst the unit tests use the mocked credentials, the end to end tests require a real set of Trello credentials (no changes to the main Trello board will be made).

## Github Actions

GitHub actions are used to build and test the project on pushes as well as when a PR is raised. If you wish to fork the repo and set up the Github actions, you will need to create secrets for the following variables:

* DOCKER_API_TOKEN
* HEROKU_API_KEY
* HEROKU_DEPLOY_EMAIL
* TRELLO_SERVER_TOKEN
* TRELLO_API_KEY
* TRELLO_WORKSPACE_ID

In addition, the following two variables are set in the ci.yml workflow and may need to be changed for your specific fork:

* DOCKER_USERNAME
* HEROKU_APP_NAME
