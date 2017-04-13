#!/usr/bin/csh
set years = "1984 1985 1986 1987 1988 1989 1990 1991 1992 1993 1994 1995 1996 1997 1998 1999 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011"
#set years = "2000"
#set months = "01"
set months = "01 02 03 04 05 06 07 08 09 10 11 12"

#These are the indices for the longitude latitude bands. These will be made into command line arguments using the output from a python script to relate the longitude and latitude bounds of the ensemble files to the wfdei indices. We can't use the longitudes and latitudes directly because the jules forcing files do not contain them. 
#set lonmin = 354
#set lonmax = 363
#set latmin = 190
#set latmax = 205

set lonmin = $1
set lonmax = $2
set latmin = $3
set latmax = $4

set global_forcingdir = $5
set local_forcingdir = $6
set jules_dir = $7

#This is the directory on the met system where the wfdei files are kept
#set global_forcingdir = /panfs/jasmin/jules/robin/WFDEI/
#set local_forcingdir = /net/elm/export/elm/data-09/emily/wfdei_test/
#set jules_dir = /net/elm/export/elm/data-09/emily/jules/wfdei_emily/





rm -f $jules_dir/*.regional.*

ncks -d lon,$lonmin,$lonmax -d lat,$latmin,$latmax $jules_dir/WFD\-EI\-LandFraction2d-2.nc landfrac.regional.nc
ncks -d lon,$lonmin,$lonmax -d lat,$latmin,$latmax $jules_dir/qrparm.veg.frac2d-2.nc vegfrac.regional.nc
ncks -d lon,$lonmin,$lonmax -d lat,$latmin,$latmax $jules_dir/qrparm.soil_HWSD_class3_van_genuchten2d-2.nc soil.regional.nc
ncks -d lon,$lonmin,$lonmax -d lat,$latmin,$latmax $jules_dir/WFDEI-long-lat-2d-2.nc lonlat.regional.nc 

#this is the local copy of the subsetted wfdei driving files referred to in the driving file name list
#cd $local_forcingdir
rm -f  $local_forcingdir/*/*regional*

foreach year ($years)
foreach month ($months)
echo $year $month

echo $global_forcingdir/LWdown_WFDEI/LWdown_WFDEI_$year$month.nc

ncks -d lon,$lonmin,$lonmax -d lat,$latmin,$latmax $global_forcingdir/LWdown_WFDEI/LWdown_WFDEI_$year$month.nc $local_forcingdir/LWdown_regional/LWdown_regional_$year$month.nc
ncks -d lon,$lonmin,$lonmax -d lat,$latmin,$latmax $global_forcingdir/SWdown_WFDEI/SWdown_WFDEI_$year$month.nc $local_forcingdir/SWdown_regional/SWdown_regional_$year$month.nc
ncks -d lon,$lonmin,$lonmax -d lat,$latmin,$latmax $global_forcingdir/PSurf_WFDEI/PSurf_WFDEI_$year$month.nc $local_forcingdir/PSurf_regional/PSurf_regional_$year$month.nc
ncks -d lon,$lonmin,$lonmax -d lat,$latmin,$latmax $global_forcingdir/Qair_WFDEI/Qair_WFDEI_$year$month.nc $local_forcingdir/Qair_regional/Qair_regional_$year$month.nc
ncks -d lon,$lonmin,$lonmax -d lat,$latmin,$latmax $global_forcingdir/Rainf_WFDEI_CRU/Rainf_WFDEI_CRU_$year$month.nc $local_forcingdir/Rainf_regional/Rainf_regional_$year$month.nc
ncks -d lon,$lonmin,$lonmax -d lat,$latmin,$latmax $global_forcingdir/Snowf_WFDEI_CRU/Snowf_WFDEI_CRU_$year$month.nc $local_forcingdir/Snowf_regional/Snowf_regional_$year$month.nc
ncks -d lon,$lonmin,$lonmax -d lat,$latmin,$latmax $global_forcingdir/Tair_WFDEI/Tair_WFDEI_$year$month.nc $local_forcingdir/Tair_regional/Tair_regional_$year$month.nc
ncks -d lon,$lonmin,$lonmax -d lat,$latmin,$latmax $global_forcingdir/Wind_WFDEI/Wind_WFDEI_$year$month.nc $local_forcingdir/Wind_regional/Wind_regional_$year$month.nc

end
end
#cp Rainf_regional/Rainf_regional_$year$month.nc $jules_dir
#cd $jules_dir
#mv Rainf_regional_$year$month.nc examplefile.nc

#changed variable templating in drive.nml
#changed input grid dimensions in model_grid.nml

#changed name of lon/lat file in model_grid.nml
#changed land frac file in model_grid.nml

#changed veg_frac file in ancilliaries.nml
#changed soil properties file in ancillaries.nml
