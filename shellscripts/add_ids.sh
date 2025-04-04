#!/bin/bash

echo "adding xml:ids"

add-attributes -g "data/editions/*.xml" -b "https://parlamint-at.acdh.oeaw.ac.at"
add-attributes -g "data/indices/*.xml" -b "https://parlamint-at.acdh.oeaw.ac.at"
add-attributes -g "data/meta/*.xml" -b "https://parlamint-at.acdh.oeaw.ac.at"