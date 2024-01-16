#!/bin/bash

export PASSWORD=$1

source .env/bin/activate
python migrationtools/documentdb_index_tool.py \
--dump-indexes --dir ./index/  \
--uri mongodb://root_2:$PASSWORD@localhost:27017
