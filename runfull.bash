#!/bin/bash

opath=~/data/h5files

[ -d "$opath" ] || mkdir -p $opath
outfile=${opath}/sim_128e_128a.h5
./src/run_sim.py -ofname ${outfile} 
