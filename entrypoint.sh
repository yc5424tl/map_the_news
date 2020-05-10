#!/usr/bin/env bash
#SEC_KEY=$( cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 32 )
SEC_KEY=$( cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 32 )
export SECRET_KEY=${SEC_KEY}
gunicorn geodjango_news_map.wsgi:application --bind 0.0.0.0:"${PORT}"