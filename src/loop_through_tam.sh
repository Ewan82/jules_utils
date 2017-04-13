#!/bin/bash

orig_dat_dir=$1
out_dat_dir=$2

for i in {2005..2011};
    do for j in 0{1..9} {10..12};
        #./jules/plot_code/src/subset_tamsat_rain.sh
        do ./jules/plot_code/src/subset_tamsat_rain.sh $i $j ${orig_dat_dir}$i/$j/ ${out_dat_dir}$i/$j/;
done
done