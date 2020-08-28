docker cp ../app/mtn_web/static/js map_the_news_web_1:/home/app/web/staticfiles/js
echo "python3 manage.py collectstatic --noinput" | docker exec -i map_the_news_web_1 bash