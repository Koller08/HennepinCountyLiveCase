## Convert tract file to lat, lng
library(tidyverse)
library(dplyr)
library(rgdal)
library(leafletR)

setwd("D:/UMN/06_6130 Introduction to Business Analytics in R/Hennepin County Live Case")

hennepin = readOGR(dsn = "map_data", layer = "2010_Census_Tracts")

retail_US <- read_csv("SNAP_Store_Locations.csv")
retail_US$Zip5 <- as.numeric(retail_US$Zip5)
retail <- retail_US %>%
  filter(State == 'MN', County == 'HENNEPIN')

cord.dec <- SpatialPoints(retail[, c("Longitude", "Latitude")], 
                          proj4string = CRS("+proj=longlat"))
lnglat <- spTransform(cord.dec, hennepin@proj4string@projargs)
spdf_retail <- SpatialPointsDataFrame(lnglat, retail)

# ---------------------------------------

# reference
# https://gis.stackexchange.com/questions/31743/projecting-sp-objects-in-r

hennipin_transformed <- spTransform(hennepin, CRS("+proj=longlat"))
toGeoJSON(hennipin_transformed, 'hennepin')

# finally, use following to transfer geojson to topojson
# https://mapshaper.org/

