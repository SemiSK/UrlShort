#!bin/bash
docker-compose up -d
docker exec -it shortener /etc/init.d/nginx restart