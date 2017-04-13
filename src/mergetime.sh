#!/bin/bash

module load cdo

for i in {2005..2011};
    do for j in 0{1..9} {10..12};
        do cdo mergetime ~/tamsat_rain_gh/$i/$j/*.nc ~/tamsat_rain_gh/$i/$j/rfe_"$i"_"$j".nc;
        done;
    done