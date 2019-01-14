FROM python:3.6
MAINTAINER Komal Thareja<komal.thareja@gmail.com>

RUN apt-get update && apt-get install -y \
  postgresql-client \
  && pip install virtualenv \
  && mkdir /code/

WORKDIR /code
VOLUME ["/code"]
ENTRYPOINT ["/code/docker-entrypoint.sh"]
