docker cp ../app/mtn_web/static/css map_the_news_web_1:/home/app/web/staticfiles/css
echo "python3 manage.py collectstatic --noinput" | docker exec -i map_the_news_web_1 bash