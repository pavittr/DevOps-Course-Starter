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

ENTRYPOINT ["./prod_entrypoint.sh"]

FROM base as test

RUN apt-get update -qqy && apt-get install -qqy wget gnupg unzip
# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
 && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
 && apt-get update -qqy \
 && apt-get -qqy install google-chrome-stable \
 && rm /etc/apt/sources.list.d/google-chrome.list \
 && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
# Install Chrome WebDriver
RUN CHROME_MAJOR_VERSION=$(google-chrome --version | sed -E "s/.* ([0-9]+)(\.[0-9]+){3}.*/\1/") \
 && CHROME_DRIVER_VERSION=$(wget --no-verbose -O - "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_MAJOR_VERSION}") \
 && echo "Using chromedriver version: "$CHROME_DRIVER_VERSION \
 && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
 && unzip /tmp/chromedriver_linux64.zip -d /usr/bin \
 && rm /tmp/chromedriver_linux64.zip \
 && chmod 755 /usr/bin/chromedriver

# Install Firefox
RUN apt-get update && apt-get install -y firefox-esr
#Install Firefox WebDriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz \
 && tar -C /usr/bin -xvzf /app/geckodriver-v0.30.0-linux64.tar.gz
#Set to ensure Firefox doesn't try and load a display in the container
ENV MOZ_HEADLESS=1

ENTRYPOINT ["poetry", "run", "pytest"]
