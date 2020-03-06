#!/bin/bash
set -x

rm -rf ./verify-core/verify/migrations/*
rm -f ./verify-core/db.sqlite3
./verify-core/manage.py makemigrations verify
./verify-core/manage.py migrate