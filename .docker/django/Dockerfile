# ==============================
FROM python:3.9 as base
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

# ==============================
FROM base as development
# ==============================

COPY --chown=appuser:appuser dev-requirements.txt .

RUN pip install -r dev-requirements.txt --no-cache-dir

COPY --chown=appuser:appuser . .

ENTRYPOINT ["/app/.docker/django/docker-entrypoint.sh"]

USER appuser:appuser

EXPOSE 8000
