#!/bin/bash

opath=~/data/h5files
nthreads=4
nangles=16
nimages=128
nenergies=360

[ -d "$opath" ] || mkdir -p $opath
outfile=${opath}/out_${nenergies}e_${nangles}a.h5
./src/run_simulation.py ${outfile} $nimages $nangles ${nthreads}   
