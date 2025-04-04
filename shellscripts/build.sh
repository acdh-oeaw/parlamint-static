#!/bin/bash

./shellscripts/dl_imprint.sh
./shellscripts/add_ids.sh

echo "creating oai-pmh files"
python oai-pmh/make_files.py
ant