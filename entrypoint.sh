#!/usr/bin/env bash
#SEC_KEY=$( cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 32 )
SEC_KEY=$( cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 32 )
export SECRET_KEY=${SEC_KEY}
echo 'Collecting Static Files'
python3 manage.py collectstatic --no-input
echo 'Applying Database Migrations'
python3 manage.py migrate --noinput
echo 'Starting Server'
gunicorn mtn_core.wsgi:application --bind 0.0.0.0:"${PORT}"