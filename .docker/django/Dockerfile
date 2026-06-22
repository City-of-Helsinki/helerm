# ==============================
FROM registry.access.redhat.com/ubi9/python-312 AS appbase
# ==============================

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.11.23@sha256:d0a0a753ab981624b49c97abc98821c1c09f4ca69d1ef5cee69c501be3d88479 /uv /uvx /usr/local/bin/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV UV_PROJECT_ENVIRONMENT=/opt/app-root \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1 \
    UV_PYTHON_DOWNLOADS=never

# Make the virtualenv binaries available on PATH
ENV PATH="/opt/app-root/bin:$PATH"

WORKDIR /app

USER root

COPY pyproject.toml uv.lock ./

RUN dnf update -y && dnf install -y \
    gettext \
    && uv sync --frozen --no-dev --group prod --no-install-project \
    && uwsgi --build-plugin https://github.com/City-of-Helsinki/uwsgi-sentry \
    && mkdir -p /usr/local/lib/uwsgi/plugins \
    && mv sentry_plugin.so /usr/local/lib/uwsgi/plugins/ \
    && dnf clean all


ENTRYPOINT ["/app/.docker/django/docker-entrypoint.sh"]

# ==============================
FROM appbase AS development
# ==============================

RUN uv sync --frozen --group dev --group prod --no-install-project

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
