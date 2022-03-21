FROM python:3.10

WORKDIR /ism
COPY /src src
COPY /scripts/wait-for-it.sh .
COPY setup.py setup.cfg README.rst CHANGELOG.rst logging.conf .

RUN pip install -e .

