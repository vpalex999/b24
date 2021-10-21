FROM python:3.8

COPY . /utils
RUN pip install -r /utils/requirements.txt
WORKDIR /utils