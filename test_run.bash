#!/bin/bash

opath=/sdf/scratch/${USER}/CookieSimSlim_data  
mkdir -p ${opath}  
outfile=${opath}/test.h5  
python3 ./src/run_simulation.py -ofname ${outfile} -n_threads 2 -n_images 20 -n_angles 32 -n_energies 512 -polstrength 1 -polstrengthvar 1 -centralenergy 256 -centralenergyvar 128 -kickstrength 128 -kickstrengthvar 64 -drawscale 1

