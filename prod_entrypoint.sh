#!/bin/bash -ex


poetry run gunicorn -b 0.0.0.0:${PORT:-8000} -w 4 "todo_app.app:create_app()"
