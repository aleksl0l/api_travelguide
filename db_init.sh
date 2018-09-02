#!/usr/bin/env bash
echo 'Preparing Postgres'
sudo su postgres -c "psql -c \"CREATE DATABASE ${1:-travel}\" "
sudo su postgres -c "psql -c \"CREATE USER ${1:-travel} WITH PASSWORD '${1:-travel}'\" "
sudo su postgres -c "psql -c \"ALTER ROLE ${1:-travel} WITH CREATEDB\" "
sudo su postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE ${1:-travel} to ${1:-travel}\" "
