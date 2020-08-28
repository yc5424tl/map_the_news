
cmd_1="python3 manage.py makemigrations;"
cmd_2="python3 manage.py migrate admin;"
cmd_3="python3 manage.py migrate auth;"
cmd_4="python3 manage.py migrate contenttypes;"
cmd_5="python3 manage.py migrate mtn_web;"
cmd_6="python3 manage.py migrate sessions"
echo "$cmd_1$cmd_2$cmd_3$cmd_4$cmd_5$cmd_6" | docker exec -i map_the_news_web_1 bash

# ip=${docker inspect mtn_web_1 | grep -e '"Gateway"'}
# echo "export MTN_WEB_1_IP=${ip}" | docker exec -i mtn_web_1 bash