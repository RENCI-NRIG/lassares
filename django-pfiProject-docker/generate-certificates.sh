#!/usr/bin/env bash

ROOT_DIR=$(pwd)

if [ ! -d $ROOT_DIR/certs ]; then
  mkdir -p $ROOT_DIR/certs
else
  rm -f $ROOT_DIR/certs/*
fi

cd $ROOT_DIR/certs
openssl req -x509 -newkey rsa:2048 -sha256 -days 365 -nodes \
  -keyout self.signed.key -out self.signed.crt -config $ROOT_DIR/req.cnf 
cd -

exit 0;
