#!/bin/bash
docker image prune -f
docker stop core-wolfbolin
docker rm core-wolfbolin
echo -e "\033[5;36mOrz 旧容器(镜像)已清理\033[0m"

time_now=$(date "+%m%d%H")
docker build -f Dockerfile --tag core-wolfbolin:"${time_now}" .
echo -e "\033[5;36mOrz 镜像重建完成\033[0m"

docker run -itd \
	-p 12864:80 \
	--restart always \
	--name core-wolfbolin\
	-v "$(pwd)":/var/app \
	core-wolfbolin:"${time_now}"
echo -e "\033[5;36mOrz 镜像启动完成\033[0m"
docker ps -a
docker logs core-wolfbolin -f
