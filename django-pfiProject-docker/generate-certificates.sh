#!/usr/bin/env bash

ROOT_DIR=$(pwd)

if [ ! -d $ROOT_DIR/certs ]; then
  mkdir -p $ROOT_DIR/certs
else
  rm -f $ROOT_DIR/certs/*
fi

cd $ROOT_DIR/certs
openssl req -newkey rsa:4096 -days 365 -nodes -x509 \
  -subj "/C=US/ST=North Carolina/L=Chapel Hill/O=Local/OU=Development/CN=local.dev/emailAddress=email@local.dev" \
  -keyout self.signed.key \
  -out self.signed.crt
cd -

exit 0;
