#!/usr/bin/env bash

# See https://portal.opentopography.org/datasetMetadata?otCollectionID=OT.032021.4326.1

###### copernicus #######
# download dems
aws s3 cp s3://raster/COP90/ data/dem --recursive --endpoint-url https://opentopography.s3.sdsc.edu --no-sign-request
# sync (download missing dems)
aws s3 sync s3://raster/COP90/ data/dem --recursive --endpoint-url https://opentopography.s3.sdsc.edu --no-sign-request

####### gebco 2021 ########
# other interesting data in https://www.gebco.net/data_and_products/gridded_bathymetry_data


####### SF bay topography/bathymetery ###########
# https://www.usgs.gov/core-science-systems/eros/coned/science/topobathymetric-elevation-model-san-francisco-bay-area?qt-science_center_objects=0#qt-science_center_objects
# https://topotools.cr.usgs.gov/topobathy_viewer/dwndata.htm
wget https://edcintl.cr.usgs.gov/downloads/sciweb1/shared/topo/downloads/Topobathy/TOPOBATHY_SAN_FRANCISCO_ELEV_METERS.zip

########## greenland (measures project) ##########
# https://nsidc.org/data/nsidc-0715/versions/1
# https://nsidc.org/order-history
