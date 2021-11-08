#!/bin/bash

opath=~/data/h5files
nthreads=20
nimages=50000

[ -d "$opath" ] || mkdir -p $opath
outfile=${opath}/sim_128e_128a.h5
./src/run_sim.py -ofname ${outfile} -n_images $nimages -n_threads $nthreads   
