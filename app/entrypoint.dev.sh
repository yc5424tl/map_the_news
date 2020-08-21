#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z ${DB_HOST} ${DB_PORT}; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

/usr/bin/python3 manage.py collectstatic --noinput

exec "$@"

####################################################
#                                                  #
#  update file permission after this file is made  #
#  $ chmod +x app/entrypoint.dev.sh                #
#                                                  #
####################################################
