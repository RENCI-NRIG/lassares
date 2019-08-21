FROM python:3.7
MAINTAINER Komal Thareja<komal.thareja@gmail.com>

RUN apt-get update && apt-get install -y \
  binutils \
  libproj-dev \
  gdal-bin \
  postgresql-client \
  && pip install virtualenv \
  && mkdir /code/

WORKDIR /code
VOLUME ["/code"]
ENTRYPOINT ["/code/docker-entrypoint.sh"]
