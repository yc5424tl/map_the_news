#!/usr/bin/env bash
#SEC_KEY=$( cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 32 )
SEC_KEY=$( cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 32 )
export SECRET_KEY=${SEC_KEY}
echo 'Starting Server'
gunicorn mtn_core.wsgi:application --bind 0.0.0.0:"${PORT}"