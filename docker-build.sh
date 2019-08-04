#!/bin/bash
docker stop wb_website
docker rm wb_website
docker rmi wb_website:latest

docker build --tag wb_website:latest .
docker run -itd --name wb_website -p 25680:25680 wb_website
docker ps -a
docker logs wb_website -f
