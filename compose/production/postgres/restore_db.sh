#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username $POSTGRES_USER <<-EOSQL
    DROP DATABASE IF EXISTS nrgx_app;
    DROP ROLE IF EXISTS nrgx_app;

    CREATE USER nrgx_app;
    CREATE DATABASE nrgx_app;
    GRANT ALL PRIVILEGES ON DATABASE nrgx_app TO nrgx_app;

    ALTER USER nrgx_app WITH PASSWORD 'nrgx_app';
EOSQL

pg_restore -U nrgx_app -d nrgx_app -c -v ./nrgx_sql