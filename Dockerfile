# Dockerfile for helerm backend
# Attemps to provide for both local development and server usage

ARG PROJECT_NAME=helerm

FROM python:3.7-buster as appbase
ARG PROJECT_NAME

RUN useradd -ms /bin/bash -d /$PROJECT_NAME $PROJECT_NAME

WORKDIR /$PROJECT_NAME

# Can be used to inquire about running app
# eg. by running `echo $APP_NAME`
ENV APP_NAME $PROJECT_NAME
# This is server out by Django itself, but aided
# by whitenoise by adding cache headers and also delegating
# much of the work to WSGI-server
ENV STATIC_ROOT /srv/static

# less & netcat-openbsd are there for in-container manual debugging
RUN apt-get update && \
    apt-get install -y postgresql-client less netcat-openbsd gettext && \
    apt-get clean

RUN pip install --no-cache-dir uwsgi
# Sentry CLI for sending events from non-Python processes to Sentry
# eg. https://docs.sentry.io/cli/send-event/#bash-hook
RUN curl -sL https://sentry.io/get-cli/ | bash

# Copy requirements files to image for preloading dependencies
# in their own layer
COPY requirements.txt .

# deploy/requirements.txt must reference the base requirements
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Statics are kept inside container image (as opposed to CDN or bucket)
# for serving using whitenoise
RUN mkdir -p /srv/static && python manage.py collectstatic

# Localized messages
RUN ./manage.py compilemessages

# Our entrypoint provides a CLI like UX
ENTRYPOINT ["deploy/entrypoint.sh"]

#Both production and dev servers listen on port 8000
EXPOSE 8000

# Next, the development & testing extras
FROM appbase as development
ARG PROJECT_NAME

RUN pip install --no-cache-dir -r dev-requirements.txt

# Entrypoint handles this
CMD ["start_django_development_server"]

USER $PROJECT_NAME

# And the production image
FROM appbase as production
ARG PROJECT_NAME

USER $PROJECT_NAME
