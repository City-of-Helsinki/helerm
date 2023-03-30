#!/bin/bash

set -e

if [[ "$WAIT_FOR_IT_HOSTS" ]]; then
    echo "Waiting for hosts: $WAIT_FOR_IT_HOSTS"
    for host in $WAIT_FOR_IT_HOSTS; do
        ./.docker/tools/wait-for-it/wait-for-it.sh "$host" -t 30
    done
fi

if [[ "$APPLY_MIGRATIONS" = "True" ]]; then
    echo "Applying migrations..."
    ./manage.py migrate --noinput
fi

if [[ "$CREATE_SUPERUSER" = "True" ]]; then
    ./manage.py create_superuser --noinput
fi

# Start server
if [[ -n "$*" ]]; then
    "$@"
elif [[ "$DEV_SERVER" = "True" ]]; then
    python -Wd ./manage.py runserver 0.0.0.0:8000
else
    uwsgi --ini /app/.docker/django/uwsgi_configuration.ini
fi
