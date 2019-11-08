#!/usr/bin/env bash

ROOT_DIR=$(pwd)

if [ ! -d $ROOT_DIR/certs ]; then
  mkdir -p $ROOT_DIR/certs
else
  rm -f $ROOT_DIR/certs/*
fi

cd $ROOT_DIR/certs
openssl req -newkey rsa:2048 -days 365 -nodes -x509 \
  -subj "/C=US/ST=North Carolina/L=Chapel Hill/O=RENCI/OU=NRIG/CN=your.domain.com/emailAddress=jmpmcman@renci.org" \
  -keyout self.signed.key \
  -out self.signed.crt
cd -

exit 0;
