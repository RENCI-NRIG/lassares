#!/bin/sh
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi -f $(docker images -q)
docker network rm $(docker network ls --format "{{.ID}}")
#mvn clean install
rm -rf .venv
find . -name __pycache__ | xargs rm -rf
rm -rf static/admin/ static/geoposition/
