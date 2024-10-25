FROM python:3.11-alpine

WORKDIR /devops
COPY python/uploaders/* /devops/
COPY requirements.txt /devops/
RUN pip install -r requirements.txt