#!/usr/bin/env bash
set -e

if [ $# -ne 1 ]; then
    echo "Required arguments [GOOGLE_API_KEY] not provided!"
    exit 1
fi

mkdir -p /var/www
cp -R /root/lassares/django-pfiProject-docker /var/www
chown -R root:root /var/www/
chmod -R g+w /var/www/
cd /var/www/django-pfiProject-docker/
/var/www/django-pfiProject-docker/generate-certificates.sh

LOCALIP=`/opt/aws/bin/ec2-metadata -o|cut -d' ' -f2`

GOOGLE_API_KEY=$1

echo "enable for docker service"
chkconfig --add docker
echo "start docker service"
service docker start

curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

echo "" > /var/www/django-pfiProject-docker/pfiProject/secrets/secrets.py
echo "GOOGLE_MAP_API_KEY='$GOOGLE_API_KEY'" >> /var/www/django-pfiProject-docker/pfiProject/secrets/secrets.py
SECRET=`uuidgen`
echo "SECRET_KEY='$SECRET'" >> /var/www/django-pfiProject-docker/pfiProject/secrets/secrets.py
echo "RUN_ROOT=1" >> /var/www/django-pfiProject-docker/pfiProject/.env

NGINX_HOST=$LOCALIP docker-compose up -d

sleep 1m

docker container exec -i database psql -U postgres -d postgres < /var/www/django-pfiProject-docker/data/drf_fdr_18001_0_11.sql
docker container exec -i database psql -U postgres -d postgres < /var/www/django-pfiProject-docker/data/meas_web_measurement.sql

