#!/usr/bin/env bash

# See https://portal.opentopography.org/datasetMetadata?otCollectionID=OT.032021.4326.1

# download all dems
aws s3 cp s3://raster/COP90/ data/dem --recursive --endpoint-url https://opentopography.s3.sdsc.edu --no-sign-request

# sync
#aws s3 sync s3://raster/COP90/ data/dem --recursive --endpoint-url https://opentopography.s3.sdsc.edu --no-sign-request
