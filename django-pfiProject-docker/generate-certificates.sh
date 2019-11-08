#!/usr/bin/env bash

ROOT_DIR=$(pwd)

if [ ! -d $ROOT_DIR/certs ]; then
  mkdir -p $ROOT_DIR/certs
else
  rm -f $ROOT_DIR/certs/*
fi

cd $ROOT_DIR/certs
openssl req -x509 -newkey rsa:2048 -sha256 -days 3650 -nodes \
  -keyout self.signed.key -out self.signed.crt \
  -subj "/C=US/ST=North Carolina/L=Chapel Hill/O=RENCI/OU=NRIG/CN=example.com/emailAddress=jmpmcman@renci.org/" \
  -addext "subjectAltName=DNS:example.com,DNS:example.com,IP:10.0.0.1"
cd -

exit 0;
