FROM python:3.4-stretch
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN apt-get update && apt-get install -y \
    gettext \
    postgresql-client-9.6

ADD requirements.txt /code/
ADD dev-requirements.txt /code/
RUN pip install -r /code/requirements.txt -r /code/dev-requirements.txt --no-cache-dir

COPY . /code/
