#!/usr/bin/env bash
echo 'Preparing Postgres'
sudo su postgres -c "psql -c \"CREATE DATABASE ${1:-travel}\" "
sudo su postgres -c "psql -c \"CREATE USER travel WITH PASSWORD '${1:-travel}'\" "
sudo su postgres -c "psql -c \"ALTER ROLE travel WITH CREATEDB\" "
sudo su postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE ${1:-travel} to travel\" "
