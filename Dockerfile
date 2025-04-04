FROM python:3.12.2

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install -r "requirements.txt"

RUN apt-get update  && apt-get install -y postgresql-client

COPY . .
