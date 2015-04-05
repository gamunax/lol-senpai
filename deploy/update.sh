#!/bin/sh

git pull

docker stop lol-senpai
docker rm -f lol-senpai
docker rmi -f lol-senpai

docker build -t lol-senpai .
docker run --name lol-senpai -p 5000:5000 -d lol-senpai
