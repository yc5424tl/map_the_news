#!/bin/bash

docker cp ../db/dump/latest.dump map_the_news_db_1:./

echo "pg_restore --verbose --clean --no-acl --no-owner -U $DB_USER -d $DB_DATABASE latest.dump" | docker exec -i map_the_news_db_1 sh

