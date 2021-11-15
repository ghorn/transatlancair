#!/usr/bin/env bash

# See https://portal.opentopography.org/datasetMetadata?otCollectionID=OT.032021.4326.1

# download all dems
aws s3 cp s3://raster/COP90/ data/dem --recursive --endpoint-url https://opentopography.s3.sdsc.edu --no-sign-request

# sync
#aws s3 sync s3://raster/COP90/ data/dem --recursive --endpoint-url https://opentopography.s3.sdsc.edu --no-sign-request

# other interesting data in https://www.gebco.net/data_and_products/gridded_bathymetry_data


# Good SF bay topography/bathymetery.
# https://topotools.cr.usgs.gov/topobathy_viewer/dwndata.htm
wget https://edcintl.cr.usgs.gov/downloads/sciweb1/shared/topo/downloads/Topobathy/TOPOBATHY_SAN_FRANCISCO_ELEV_METERS.zip
