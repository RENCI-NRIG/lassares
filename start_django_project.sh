#!/usr/bin/env bash
yum update -y
yum -y install jq

set -e

if [ $# -ne 4 ]; then
    echo "Required arguments [MBTOKEN], [CLIENTID] [AUTH0DOMAIN], and [APIIDENTIFIER] not provided!"
    exit 4
fi

mkdir -p /var/www
cp -R /root/lassares/django-pfiProject-docker /var/www
chown -R root:root /var/www/
chmod -R g+w /var/www/
cd /var/www/django-pfiProject-docker/

LOCALIP=`/opt/aws/bin/ec2-metadata -o|cut -d' ' -f2`
PUBHOSTDOMAIN=`/opt/aws/bin/ec2-metadata -p|cut -d' ' -f2`
MBTOKEN=$1
CLIENTID=$2
AUTH0DOMAIN=$3
APIIDENTIFIER=$4

echo "enable for docker service"
chkconfig --add docker
echo "start docker service"
service docker start

curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

echo "" > /var/www/django-pfiProject-docker/pfiProject/secrets/secrets.py
SECRET=`uuidgen`
echo "SECRET_KEY='$SECRET'" >> /var/www/django-pfiProject-docker/pfiProject/secrets/secrets.py
echo "PUBHOST_URL='$PUBHOSTDOMAIN'" >> /var/www/django-pfiProject-docker/pfiProject/secrets/secrets.py
echo "AUTH0_DOMAIN='$AUTH0DOMAIN'" >> /var/www/django-pfiProject-docker/pfiProject/secrets/secrets.py
echo "API_IDENTIFIER='$APIIDENTIFIER'" >> /var/www/django-pfiProject-docker/pfiProject/secrets/secrets.py

SECRETSFILE="/var/www/django-pfiProject-docker/quasar/src/assets/secrets.json"
SECRETSTMP="/var/www/django-pfiProject-docker/quasar/src/assets/secretstmp.json"
cat $SECRETSFILE | MBTOKEN="$MBTOKEN" jq 'map(if .MB_KEY == "YOU NEED TO REPLACE THIS WITH A MAP BOX TOKEN" then . + {"MB_KEY":env.MBTOKEN} else . end)' > $SECRETSTMP && mv $SECRETSTMP $SECRETSFILE
cat $SECRETSFILE | CLIENTID="$CLIENTID" jq 'map(if .CLIENT_ID == "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" then . + {"CLIENT_ID":env.CLIENTID} else . end)' > $SECRETSTMP && mv $SECRETSTMP $SECRETSFILE
cat $SECRETSFILE | AUTH0DOMAIN="$AUTH0DOMAIN" jq 'map(if .AUTH0_DOMAIN == "xxxxxxxxxx.auth0.com" then . + {"AUTH0_DOMAIN":env.AUTH0DOMAIN} else . end)' > $SECRETSTMP && mv $SECRETSTMP $SECRETSFILE
cat $SECRETSFILE | APIIDENTIFIER="$APIIDENTIFIER" jq 'map(if .API_IDENTIFIER == "https://xxxxxxxx" then . + {"API_IDENTIFIER":env.APIIDENTIFIER} else . end)' > $SECRETSTMP && mv $SECRETSTMP $SECRETSFILE

PUBHOSTFILE="/var/www/django-pfiProject-docker/quasar/src/assets/pubhost.json"
PUBHOSTTMP="/var/www/django-pfiProject-docker/quasar/src/assets/pubhosttmp.json"
cat $PUBHOSTFILE | PUBHOSTDOMAIN="$PUBHOSTDOMAIN" jq 'map(if .PUBHOST_URL == "127.0.0.1:8443" then . + {"PUBHOST_URL":env.PUBHOSTDOMAIN} else . end)' > $PUBHOSTTMP && mv $PUBHOSTTMP $PUBHOSTFILE

echo "RUN_ROOT=1" >> /var/www/django-pfiProject-docker/pfiProject/.env

#NGINX_HOST=$LOCALIP docker-compose up -d
NGINX_HOST=$PUBHOSTDOMAIN docker-compose up -d

sed -i 's/example.com/'$PUBHOSTDOMAIN'/g' /var/www/django-pfiProject-docker/init-letsencrypt.sh
#sed -i 's/10.0.0.1/'$LOCALIP'/g' /var/www/django-pfiProject-docker/init-letsencrypt.sh
/var/www/django-pfiProject-docker/init-letsencrypt.sh

sleep 3m

docker container exec -i database psql -U postgres -d postgres < /var/www/django-pfiProject-docker/data/drf_fdr_18001_0_11.sql
docker container exec -i database psql -U postgres -d postgres < /var/www/django-pfiProject-docker/data/meas_web_measurement.sql

