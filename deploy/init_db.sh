#!/bin/sh
# dbshell can make use of DATABASE_URL
# create extension both into the already created database
# and template1 (for pytest)
./manage.py dbshell << EOSQL
CREATE EXTENSION IF NOT EXISTS hstore;
\c template1
CREATE EXTENSION IF NOT EXISTS hstore;
EOSQL

