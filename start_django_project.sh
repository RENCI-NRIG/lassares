#!/usr/bin/env bash
yum update -y
yum -y install jq

set -e

if [ $# -ne 2 ]; then
    echo "Required arguments [GOOGLE_API_KEY] [MBTOKEN] not provided!"
    exit 2
fi

mkdir -p /var/www
cp -R /root/lassares/django-pfiProject-docker /var/www
chown -R root:root /var/www/
chmod -R g+w /var/www/
cd /var/www/django-pfiProject-docker/
/var/www/django-pfiProject-docker/generate-certificates.sh

LOCALIP=`/opt/aws/bin/ec2-metadata -o|cut -d' ' -f2`
PUBHOSTURL=`/opt/aws/bin/ec2-metadata -p|cut -d' ' -f2`
GOOGLE_API_KEY=$1
MBTOKEN=$2

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
echo "PUBHOST_URL='$PUBHOSTURL'" >> /var/www/django-pfiProject-docker/pfiProject/secrets/secrets.py
MBTOKENFILE="/var/www/django-pfiProject-docker/quasar/src/assets/mbtoken.json"
MBTOKENTMP="/var/www/django-pfiProject-docker/quasar/src/assets/mbtokentmp.json"
cat $MBTOKENFILE | MBTOKEN="$MBTOKEN" jq 'map(if .MB_KEY == "YOU NEED TO REPLACE THIS WITH A MAP BOX TOKEN" then . + {"MB_KEY":env.MBTOKEN} else . end)' > $MBTOKENTMP && mv $MBTOKENTMP $MBTOKENFILE
PUBHOSTFILE="/var/www/django-pfiProject-docker/quasar/src/assets/pubhost.json"
PUBHOSTTMP="/var/www/django-pfiProject-docker/quasar/src/assets/pubhosttmp.json"
cat $PUBHOSTFILE | PUBHOSTURL="$PUBHOSTURL" jq 'map(if .PUBHOST_URL == "127.0.0.1:8443" then . + {"PUBHOST_URL":env.PUBHOSTURL} else . end)' > $PUBHOSTTMP && mv $PUBHOSTTMP $PUBHOSTFILE

echo "RUN_ROOT=1" >> /var/www/django-pfiProject-docker/pfiProject/.env

NGINX_HOST=$LOCALIP docker-compose up -d

sleep 3m

docker container exec -i database psql -U postgres -d postgres < /var/www/django-pfiProject-docker/data/drf_fdr_18001_0_11.sql
docker container exec -i database psql -U postgres -d postgres < /var/www/django-pfiProject-docker/data/meas_web_measurement.sql

