#!/bin/bash
source deploy/functions.sh

deploy/init_db.sh

# Store the error code for any failing commands.
# We still want to run all tests even if eg. lint fails
trap 'last_error_code=$?' ERR

_log_boxed "Running lint"
flake8
_log_boxed "Running tests"
pytest -ra -vvv

exit $last_error_code
