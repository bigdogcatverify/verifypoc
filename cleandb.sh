#!/bin/bash
set -xe

rm -f ./core.log ./block.log ./npm.log
rm -f ./verify-core/db.sqlite3
rm -rf ./verify-core/verify/migrations/*
rm -f ./verify-block/block.json
./verify-core/manage.py makemigrations verify
./verify-core/manage.py migrate
