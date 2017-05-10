#!/bin/bash
#set years = "2005 2006 2007 2008 2009 2010 2011"
#set years = "2000"
#set months = "01"
#set months = "01 02 03 04 05 06 07 08 09 10 11 12"

#These are the indices for the longitude latitude bands. These will be made into command line arguments using the output from a python script to relate the longitude and latitude bounds of the ensemble files to the wfdei indices. We can't use the longitudes and latitudes directly because the jules forcing files do not contain them.
lonmin=-3.5 #if decimal taken as lon/lat value in degrees, if int taken as index in array
lonmax=1.5
latmin=4.0
latmax=12.0

#set lonmin = $1
#set lonmax = $2
#set latmin = $3
#set latmax = $4

year=$1

#shopt -s nullglob
orig_dat_dir=$2ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-"$year"*
out_dat_dir=$3

#rm .$out_dat_dir*.nc

for i in $orig_dat_dir;
    #do cdo-1.6.6 sellonlatbox,$lonmin,$lonmax,$latmin,$latmax $i .$out_dat_dir${i##*/};
    #do ncks -d lon,$lonmin,$lonmax -d lat,$latmin,$latmax $i $out_dat_dir${i##*/};
    do nccopy -k 1 $i $out_dat_dir${i##*/}
    done