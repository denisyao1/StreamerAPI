#  pull official python 3.9 base image
FROM python:3.9-alpine

# Set Environment Variable
ENV PYTHONUNBUFFERED 1 #  Prevents Python from buffering stdout and stderr
ENV FLASK_APP=api


# set work directory
WORKDIR /streamerAPI

# install system dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev curl \
    && apk --update --upgrade add gcc musl-dev build-base

# install python dependencies
COPY ./requirements.txt /streamerAPI
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# copy project
COPY . /streamerAPI

# init db
RUN python -m flask db init
RUN python -m flask db migrate
RUN python -m flask db upgrade

