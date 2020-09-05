#!/bin/bash

# exec 3>&1 4>&2
# trap 'exec 2>&4 1>&3' 0 1 2 3 RETURN
# exec 1>log.out 2>&1


set -o allexport;
source ../.env.dev;
set +o allexport;

echo -e "...\n...\n..."

echo "DOCKER-COMPOSE: building..."
./start.compose.sh &
pid=$!
wait $pid
echo "......"
echo "DOCKER-COMPOSE: up!"


echo -e "...\n...\n..."


echo "DATABASE: starting..."
echo "while ! nc -z db 5432;do sleep 0.1;done;" | docker exec -i map_the_news_web_1 bash
echo "......"
echo "DATABASE: up!"


echo -e "...\n...\n..."

docker exec -i map_the_news_web_1 bash ./mtn_web/migrations/ a+x *.py

# echo "DJANGO: migrating..."
# ./start.migrate.sh &
# pid=$!
# wait $pid
# echo "......"
# echo "DJANGO: migrated!"


# echo -e "...\n...\n..."


echo "DATABASE: restoring..."
./start.db.sh &
pid=$!
wait $pid
echo "......"
echo "DATABASE: complete!"

echo -e "...\n...\n..."

echo "DATABASE: migrating..."
./start.migrate.sh &
pid=$!
wait $pid
echo "......"
echo "DATABASE: migrated!"


echo -e "...\n...\n..."


# Createsuperuser values @ env vars DJANGO_SUPERUSER_(PASSWORD - USERNAME - EMAIL - DATABASE)
echo "DJANGO: creating superuser..."
echo "python3 manage.py createsuperuser --noinput" | docker exec -i map_the_news_web_1 bash
echo "......"
echo "DJANGO: superuser created"


echo -e "...\n...\n..."


echo "DATABASE: migrating..."
./start.migrate.sh &
pid=$!
wait $pid
echo "......"
echo "DATABASE: migrated!"


echo -e "...\n...\n..."


echo "DJANGO: collecting static files..."
echo "python3 manage.py collectstatic --noinput" | docker exec -i map_the_news_web_1 bash
echo "......"
echo "DJANGO: collecting static files complete"


echo -e "...\n...\n..."

# specific to current dump file, source has already been updated
echo "Applying corrections to fields..."
echo "update mtn_web_source set language = 'ur' where language = 'ud';update mtn_web_source set language = 'de' where language = 'ch';" | docker exec -i map_the_news_db_1 psql -U $DB_USER -d $DB_DATABASE;
echo "update mtn_web_source set country = 'uy' where country = 'ur';update mtn_web_source set country = 'cn' where country = 'zh';" | docker exec -i map_the_news_db_1 psql -U $DB_USER -d $DB_DATABASE;

echo -e "...\n...\n..."
echo "Transfering alpha2 codes..."
echo "python3 manage.py transfer_a2_codes" | docker exec -i map_the_news_web_1 bash

echo -e "...\n...\n..."
echo "Deriving Display and AlphaNum names..."
echo "python3 manage.py expand_country_alpha2;" | docker exec -i map_the_news_web_1 bash

echo -e "...\n...\n..."
echo "Populating Countries..."
echo "python3 manage.py populate_countries_from_sources;" | docker exec -i map_the_news_web_1 bash

echo -e "...\n...\n..."
echo "Populating Languages..."
echo "python3 manage.py populate_languages_from_sources;" | docker exec -i map_the_news_web_1 bash


echo -e "...\n...\n..."
echo "Establishing Source & Publishing-Country relations..."
echo "python3 manage.py build_source_publishing_country_relations" | docker exec -i map_the_news_web_1 bash


echo -e "...\n...\n..."
echo "Establishing Source & Readership-Country relations..."
echo "python3 manage.py build_source_readership_country_relations" | docker exec -i map_the_news_web_1 bash


echo -e "...\n...\n..."
echo "Establishing Source & Language relations..."
echo "python3 manage.py build_source_language_relations" | docker exec -i map_the_news_web_1 bash


echo "Map The News -- Depoyment Complete"




# Set execute permission to:
#   - this file
#   - start_compose.sh
#   - any .sh file which runs during the build
#
# with --> $ chmod a+x file
