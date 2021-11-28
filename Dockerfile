FROM python:3.9

WORKDIR /ism
COPY /src src
COPY setup.py setup.cfg README.rst CHANGELOG.rst logging.conf .

RUN pip install -e .

