#!/bin/sh
# this script clean out old docker images and containers
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi -f $(docker images -q)
docker network rm $(docker network ls --format "{{.ID}}")
docker volume rm $(docker volume ls -qf dangling=true)
#mvn clean install
rm -rf .venv
find . -name __pycache__ | xargs rm -rf
rm -rf static/admin/ static/gis  static/mapwidgets  static/rest_framework 
