#!bin/bash
docker-compose up -d --build
docker exec -it shortener /etc/init.d/nginx restart