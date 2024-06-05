# ==============================
FROM registry.access.redhat.com/ubi9/python-39 as appbase
# ==============================

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

USER root

COPY requirements.txt .

RUN dnf update -y && dnf install -y \
    gettext \
    && pip install -U pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && dnf clean all

ENTRYPOINT ["/app/.docker/django/docker-entrypoint.sh"]

# ==============================
FROM appbase AS development
# ==============================

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

ENV DEV_SERVER=True

COPY . .

RUN mkdir -p /app/media && chmod -R g+w /app/media && chgrp -R root /app/media

USER default
EXPOSE 8000/tcp

# ==============================
FROM appbase AS staticbuilder
# ==============================

ENV VAR_ROOT=/app
COPY . /app
RUN ELASTICSEARCH_ANALYZER_MODE="raudikko" SECRET_KEY="only-used-for-collectstatic"  \
    python manage.py collectstatic --noinput

# ==============================
FROM appbase AS production
# ==============================

COPY --from=staticbuilder /app/static /app/static
COPY . .

RUN mkdir -p /app/media && chmod -R g+w /app/media && chgrp -R root /app/media

USER default
EXPOSE 8000/tcp
