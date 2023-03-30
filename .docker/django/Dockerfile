# ==============================
FROM python:3.9 AS appbase
# ==============================

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN useradd -Ums /bin/bash -d /appuser appuser

WORKDIR /app

COPY --chown=appuser:appuser requirements.txt .

RUN apt-get update && apt-get install -y \
    gettext \
    postgresql-client \
    && pip install -U pip \
    && pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/app/.docker/django/docker-entrypoint.sh"]

# ==============================
FROM appbase AS development
# ==============================

COPY --chown=appuser:appuser requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

ENV DEV_SERVER=True

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000/tcp

# ==============================
FROM appbase AS staticbuilder
# ==============================

ENV VAR_ROOT=/app
COPY --chown=appuser:appuser . /app
RUN ELASTICSEARCH_ANALYZER_MODE="raudikko" SECRET_KEY="only-used-for-collectstatic"  \
    python manage.py collectstatic --noinput

# ==============================
FROM appbase AS production
# ==============================

COPY --from=staticbuilder --chown=appuser:appuser /app/static /app/static
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000/tcp
