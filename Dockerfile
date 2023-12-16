FROM python:3.10-slim-buster

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .