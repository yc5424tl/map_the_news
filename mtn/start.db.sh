#!/bin/bash

docker cp ./db/dump/latest.dump mtn_db_1:./

#cho "apk add curl & pid=$!u;wait $pid;curl -o latest.dump '${DUMP_URL}' & pid=$!;wait $pid;pg_restore --verbose --clean --no-acl --no-owner -U mtn -d mtn_dev latest.dump" | docker exec -i mtn_db_1 sh

echo "pg_restore --verbose --clean --no-acl --no-owner -U mtn -d mtn_dev latest.dump" | docker exec -i mtn_db_1 sh

#echo "python3 manage.py makemigrations & pid=$!;wait $pid;python3 manage.py migrate admin;python3 manage.py migrate auth;python3 manage.py migrate sessions;python3 manage.py migrate mtn_web;python3 manage.py migrate contenttypes & pid=$!;wait $pid;python3 manage.py collectstatic --noinput;" | docker exec -i mtn_web_1 bash