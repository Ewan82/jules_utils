#!/bin/bash

module load cdo

for i in *.nc;
    do cdo remapcon,example_grid.text $i ${i%.*}'_regridded.nc';
    #do echo ${i%.*}'_regridded.nc';
    done
