#!/bin/bash

# docker-compose down && docker-compose build --no-cache -d && docker-compose up

# docker stop $(docker ps -qa) && docker system prune -af --volumes

docker-compose -f docker-compose.dev.yml up --build -d
