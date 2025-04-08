#!/bin/bash

echo "denormalicing indices"
denormalize-indices -f "./data/editions/*.xml" -i "./data/indices/*.xml" -m ".//*[@who]/@who" -x ".//tei:title[@type='sub'][1]/text()"

echo "deleting notegroups"
python process/remove_notegrp_from_back.py
