#!/bin/sh

docker stop lol-senpai
docker rm -f lol-senpai
docker rmi -f lol-senpai

git pull

docker build -t lol-senpai .
docker run --name lol-senpai -p 5000:5000 -d lol-senpai
