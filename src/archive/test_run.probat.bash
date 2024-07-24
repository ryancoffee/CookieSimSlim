#!/bin/bash

opath=/data/nvme/CookieSimSlim_data  
mkdir -p ${opath}  
python3 ./src/run_simulation.py -ofname ${opath}/test512.h5 -n_threads 16 -n_images 100 -n_angles 512 -n_energies 512 -polstrength 1 -polstrengthvar 1 -centralenergy 256 -centralenergyvar 256 -kickstrength 128 -kickstrengthvar 32 -drawscale 4

