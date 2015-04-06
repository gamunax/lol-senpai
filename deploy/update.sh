#!/bin/sh

if [ $# -eq 0 ]
then
    echo "Usage: ./deploy/update.sh API_KEY"
fi

git pull

docker stop lol-senpai
docker rm -f lol-senpai
docker rm -f lol-senpai-redis
docker rmi -f lol-senpai

docker build -t lol-senpai .
docker run --name lol-senpai-redis -d redis
docker run --name lol-senpai -p 127.0.0.1:5000:5000 --link lol-senpai-redis:redis -e "API_KEY=$1" -d lol-senpai
