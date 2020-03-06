#!/bin/bash

cd ./verify-core
/usr/bin/nohup python manage.py runserver 8001 > ../core.log 2>&1 &

cd ../verify-block/frontend
/usr/bin/nohup /usr/local/bin/npm start > ../../npm.log 2>&1 &

cd ..
/usr/bin/nohup python manage.py runserver 8000 > ../block.log 2>&1 &

cd ..