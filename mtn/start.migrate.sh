
cmd_1="python3 manage.py makemigrations;"
cmd_2="python3 manage.py migrate admin;"
cmd_3="python3 manage.py migrate auth;"
cmd_4="python3 manage.py migrate contenttypes;"
cmd_5="python3 manage.py migrate mtn_web;"
cmd_6="python3 manage.py migrate sessions"
echo "$cmd_1$cmd_2$cmd_3$cmd_4$cmd_5$cmd_6" | docker exec -i mtn_web_1 bash
