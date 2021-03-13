#!bin/bash
docker-compose up -d
docker exec -it site /etc/init.d/nginx restart