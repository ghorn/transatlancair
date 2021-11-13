#!/usr/bin/env bash

# download all dems
aws s3 cp s3://raster/COP90/ data/dem --recursive --endpoint-url https://opentopography.s3.sdsc.edu --no-sign-request

# move the unused ones away
./move_unused_dems.py

# tile the remaining ones
gdal_merge.py -o data/dem/merged.tif data/dem/COP90_hh/*.tif
