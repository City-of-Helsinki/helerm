# ==============================
FROM registry.access.redhat.com/ubi9/python-312 AS appbase
# ==============================

# Commit used to pull python-uwsgi-common.
ARG UWSGI_COMMON_REF=1a9d30d172c2c1ca00d5025a4464e98e00565c44

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

# Build and copy the shared uWSGI configuration and logging plugin.
ADD --checksum=sha256:accdf4f78840cd5b6081c3a9636e596a75e39101c937440840209f4cab798625 https://github.com/City-of-Helsinki/python-uwsgi-common/archive/${UWSGI_COMMON_REF}.tar.gz /usr/src/python-uwsgi-common.tar.gz
RUN mkdir -p /usr/src/python-uwsgi-common && \
    tar --strip-components=1 -xzf /usr/src/python-uwsgi-common.tar.gz -C /usr/src/python-uwsgi-common && \
    mkdir -p /etc/uwsgi && \
    cp /usr/src/python-uwsgi-common/uwsgi-base.ini /etc/uwsgi/uwsgi-base.ini && \
    uv run uwsgi --build-plugin /usr/src/python-uwsgi-common && \
    rm -rf /usr/src/python-uwsgi-common.tar.gz /usr/src/python-uwsgi-common

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
