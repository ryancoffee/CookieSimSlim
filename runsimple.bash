#!/bin/bash

opath=~/data/h5files
nthreads=2
nangles=128
nimages=10

[ -d "$opath" ] || mkdir -p $opath
outfile=${opath}/out_128e_${nangles}a.h5
./src/prob_dist.py ${outfile} $nimages $nangles ${nthreads}   
