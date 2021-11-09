#!/bin/bash

opath=~/data/h5files
nthreads=10
nimages=10

[ -d "$opath" ] || mkdir -p $opath
outfile=${opath}/sim_128e_128a.h5
./src/run_sim.py -ofname ${outfile} -n_images $nimages -n_threads $nthreads 
