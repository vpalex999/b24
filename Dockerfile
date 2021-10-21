FROM python:3.8

COPY . /b24
RUN pip install -r /b24/requirements.txt
WORKDIR /b24/utils/
