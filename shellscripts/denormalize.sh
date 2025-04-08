#!/bin/bash

denormalize-indices -f "./data/editions/*.xml" -i "./data/indices/*.xml" -m ".//*[@who]/@who" -x ".//tei:title[@level='main'][1]/text()"
