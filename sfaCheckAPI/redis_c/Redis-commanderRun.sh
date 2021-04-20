#!/bin/sh
## run Redis-commander
echo "Run Redis-commander"
echo "curl http://127.0.0.1:8082/"
docker run --rm --network itms_docker_default \
  -e REDIS_HOSTS=localhost:itms_docker_radis_1:6379:0,localhost:itms_docker_radis_1:6379:1,localhost:itms_docker_radis_1:6379:2 \
  --name redis-commander -d \
  -p 8082:8081 \
  rediscommander/redis-commander:latest

read -p "When you input Retuen key  'docker stop redis-commander'"
docker stop redis-commander
echo "STOP redis-commander "

###
# https://hub.docker.com/r/rediscommander/redis-commander
