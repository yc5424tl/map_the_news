docker cp ../app/mtn_web/static/css mtn_web_1:/home/app/web/staticfiles/css
echo "python3 manage.py collectstatic --noinput" | docker exec -i mtn_web_1 bash