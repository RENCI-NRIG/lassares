#!/usr/bin/env bash
set -e

if [ $# -ne 2 ]; then
    echo "Required arguments [GOOGLE_API_KEY] [BUCKETNAME] not provided!"
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
BUCKETNAME=$2

echo "enable for docker service"
chkconfig --add docker
echo "start docker service"
service docker start

curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

if [ $BUCKETNAME != "skip" ]; then
   /opt/aws/bin/ec2-metadata -o | cut -d' ' -f2 > /root/webserver.ip
   /usr/bin/aws s3 cp /root/webserver.ip s3://$BUCKETNAME/
fi

echo "" > /var/www/django-pfiProject-docker/pfiProject/secrets.py
echo "GEOPOSITION_GOOGLE_MAPS_API_KEY ='$GOOGLE_API_KEY'" >> /var/www/django-pfiProject-docker/pfiProject/secrets.py
SECRET=`uuidgen`
echo "SECRET_KEY='$SECRET'" >> /var/www/django-pfiProject-docker/pfiProject/secrets.py
sed -i 's/kafka/'$LOCALIP'/g' /var/www/django-pfiProject-docker/pfiProject/.env
echo "RUN_ROOT=1" >> /var/www/django-pfiProject-docker/pfiProject/.env

NGINX_HOST=$LOCALIP KAFKA_LISTENER=PLAINTEXT://$LOCALIP:9092 docker-compose up -d

docker container exec -i $(docker-compose ps -q database) psql -U postgres -d postgres < /var/www/django-pfiProject-docker/pfiProject/data/drf_fdr_18001_0_11.sql
docker container exec -i $(docker-compose ps -q database) psql -U postgres -d postgres < /var/www/django-pfiProject-docker/pfiProject/data/meas_web_measurement.sql

