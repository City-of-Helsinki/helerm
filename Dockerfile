FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Allows installation of postgresql-client-10 on Debian stretch which the Python images are based on
RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main' > /etc/apt/sources.list.d/pgdg.list
RUN wget -q -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt-get update && apt-get install -y \
    gettext \
    postgresql-client-10

RUN pip install -U pip

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
ADD dev-requirements.txt /code/
RUN pip install -r /code/requirements.txt -r /code/dev-requirements.txt --no-cache-dir

COPY . /code/
