docker cp ../app/mtn_web/static/js mtn_web_1:/home/app/web/staticfiles/js
echo "python3 manage.py collectstatic --noinput" | docker exec -i mtn_web_1 bash