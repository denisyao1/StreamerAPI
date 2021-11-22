#  pull official python 3.9 base image
FROM python:3.9.9-slim-buster

# Set Environment Variable
ENV PYTHONUNBUFFERED 1 #  Prevents Python from buffering stdout and stderr
ENV FLASK_APP=api


# set work directory
WORKDIR /streamerAPI

# install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# install python dependencies
COPY ./requirements.txt /streamerAPI
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


#Add Volume because of db file
# VOLUME /streamerAPI
# copy project
COPY . /streamerAPI

# init db
RUN python -m flask db upgrade

# entry point
# CMD ["python","api.py"]
