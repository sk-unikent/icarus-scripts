#!/bin/sh

docker-compose up -d
docker exec -it icarus_icarustest_1 env TERM=xterm bash -l
docker-compose down
