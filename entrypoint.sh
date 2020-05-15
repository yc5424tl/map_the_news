#!/usr/bin/env bash
#SEC_KEY=$( cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 32 )
SEC_KEY=$( cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 32 )
export SECRET_KEY=${SEC_KEY}
echo 'Collecting Static Files'
python3 manage.py collectstatic --no-input
echo 'Applying Database Migrations'
python3 manage.py makemigrations mtn_web
python3 manage.py makemigrations mtn_user
python3 manage.py migrate mtn_user --noinput
python3 manage.py migrate mtn_web --noinput
python3 manage.py migrate sessions --noinput
python3 manage.py migrate admin --noinput
python3 manage.py ensure_adminuser --username=$SU_USERNAME --email=$SU_EMAIL --password=$SU_PASSWORD
python3 manage.py ensure_sifter --username=$SIFTER_USER --email=$SIFTER_EMAIL --password=$SIFTER_PW
echo 'Starting Server'
gunicorn mtn_core.wsgi:application --bind 0.0.0.0:"${PORT}"