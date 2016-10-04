FROM python:3.5.2
MAINTAINER Henrique Lopes

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

ADD . /app/

# Installing project dependencies.
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install -r requirements_dev.txt
