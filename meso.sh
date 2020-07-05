#!/bin/bash

#path of MD on the opendata.server
path_md=https://opendata.dwd.de/weather/radar/mesocyclones/

wget -r -N -nd -np -q ${path_md}

python3 meso.py

find -size 173c -delete
