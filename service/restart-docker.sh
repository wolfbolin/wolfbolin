#!/bin/bash
docker_name="core-wolfbolin"
docker restart ${docker_name} && docker logs -f ${docker_name}