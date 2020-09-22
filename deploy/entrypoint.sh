#!/bin/bash
source deploy/functions.sh

trap 'last_error_code=$?' ERR

_log_boxed "HelERM container"

if [ "$1" = "help" ]; then
    _log "This is a container image for running HelERM backend"
    _log ""
    _log "By default a production ready server will be started using uWSGI"
    _log "You will need to provide configuration using environment variables, see"
    _log "config.env for the available variables. Especially important is the"
    _log "database configuration using DATABASE_URL"
    _log ""
    _log "In addition to the production server, there are several task commands:"
    _log "start_django_development_server: runs Django development server at port 8000"
    _log "migrate: runs Django migrations (manage.py migrate)"
    _log "test: runs Django tests (pytest)"
    _log "start_production_server: run production server (based on UWSGI) at port 8000"
    _log "maintenance_tasks: run periodic maintenance tasks, with level as parameter"
    _log ""
    _log "e {anything}: run command in shell, verbatim"
    _log ""
    _log_boxed "This container will now exit, for your convenience"

    exit 0
fi

_log "Start with \`help\` for instructions"

if [ "$1" = "start_django_development_server" ]; then
    _log_boxed "Running development server"
    exec deploy/dev_start.sh
elif [ "$1" = 'maintenance_tasks' ]; then
    shift
    exec deploy/run_maintenance.sh "$@"
elif [ "$1" = "migrate" ]; then
    _log_boxed "Running migrations"
    ./manage.py migrate
    _log_boxed "Running application specific initialization"
    deploy/init_application.sh
elif [ "$1" = "test" ]; then
    deploy/run_tests.sh
elif [ "$1" = "e" ]; then
    shift
    _log_boxed "exec'n $@"
    exec "$@"
else
    _log_boxed "Starting production server"
    exec uwsgi -y deploy/uwsgi.yml
fi

_log_boxed "HelERM entrypoint finished"

exit $last_error_code
