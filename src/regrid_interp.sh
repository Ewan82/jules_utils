#!/bin/bash

module load cdo

for i in {2005..2011};
    do for j in 0{1..9} {10..12};
        do cdo remapcon,example_grid.text ~/tamsat_rain_gh/$i/$j/rfe_"$i"_"$j".nc ~/tamsat_rain_gh/$i/$j/rfe_"$i"_"$j"_regridded.nc;
        done;
    done