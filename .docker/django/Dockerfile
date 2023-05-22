# ==============================
FROM registry.access.redhat.com/ubi9/python-39 as appbase
# ==============================

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

USER 0

COPY requirements.txt .

RUN yum update -y && yum install -y \
    gettext \
    && pip install -U pip \
    && pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/app/.docker/django/docker-entrypoint.sh"]

# ==============================
FROM appbase AS development
# ==============================

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

ENV DEV_SERVER=True

COPY . .

# Openshift runs containers with a random user so to simulate that elsewhere
# we use an arbitrary user
USER 158435:0

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

# Openshift runs containers with a random user so to simulate that elsewhere
# we use an arbitrary user
USER 158435:0

EXPOSE 8000/tcp
