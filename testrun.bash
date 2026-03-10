#!/usr/bin/bash

nimages=128
path_to_output='/nvme0/testrun/CookieSimSlim_data'
offsetthreads=0
nthreads=4
./src/run_simulation.py -ofname ${path_to_output}/css.16x128.h5 -n_threads $nthreads -n_angles 16 -n_energies 128 -n_images $nimages -centralenergy 64 -centralenergyvar 32 -kickstrength 32 -polstrength 1 -polstrengthvar 0 -offset_threads $offsetthreads 
fnum=`printf '%0*d' 3 $offsetthreads` 
fname="${path_to_output}/css.16x128.$HOSTNAME.$fnum.h5"
wait
./src/mrs_pacman.py $fname 
