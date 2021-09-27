FROM python:3.9.6-slim-buster as base

RUN apt-get update && apt-get install -y curl 

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

ENV PATH="/root/.local/bin:$PATH"

COPY poetry.toml pyproject.toml /app/

WORKDIR /app

RUN poetry install

COPY . /app

FROM base as development

EXPOSE 5000

ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]


FROM base as production

EXPOSE 8000

ENTRYPOINT ["poetry", "run", "gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "todo_app.app:create_app()"]
