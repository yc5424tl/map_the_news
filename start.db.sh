#!/bin/bash

docker cp ./db/dump/latest.dump mtn_db_1:./



echo "pg_restore --verbose --clean --no-acl --no-owner -U $DB_USER -d $DB_DATABASE latest.dump" | docker exec -i mtn_db_1 sh

