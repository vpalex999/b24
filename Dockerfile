FROM python:3.8

COPY ./utils /b24
COPY ./requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
WORKDIR /b24/
