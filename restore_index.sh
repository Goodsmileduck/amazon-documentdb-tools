#!/bin/bash

export PASSWORD=$1
export HOST=$2

source .env/bin/activate
python migrationtools/documentdb_index_tool.py \
--restore-indexes --dir ./index/  \
--uri "mongodb://root2:$PASSWORD@$HOST:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred"

