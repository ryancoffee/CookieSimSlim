#!/usr/bin/bash

opath=/media/coffee/9C33-6BBD/CookieSimSlim_tokens
nthreads=4
offset=0
nangles=16
nenergies=320
nimages=16384 #4096

# 16 angles, 128 energies, 4096 images, less than a minute to run
# and each thread/file is only 77MB, so the whole move at the end is less than 1GB

[ -d "$opath" ] || mkdir -p $opath
outfile=${opath}/css.${nangles}x${nenergies}.h5
python3 ${HOME}/projects/CookieSimSlim/src/run_simulation.py -ofname ${outfile} -n_threads ${nthreads} -offset_threads ${offset} -n_angles ${nangles} -n_energies ${nenergies} -n_images ${nimages} -centralenergy 160 -centralenergyvar 100 -kickstrength 64 -polstrength 1 -polstrengthvar 0
wait
