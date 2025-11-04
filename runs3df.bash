#!/usr/bin/bash

source /sdf/group/lcls/ds/ana/sw/conda2/manage/bin/psconda.sh

opath=/sdf/data/slac/s2ai/CookieSimSlim_tokens
nthreads=16
offset=0
nangles=16
nenergies=320
nimages=16384 #4096

# 16 angles, 320 energies, 16k images, less than three minutes to run
# and each thread/file is only 120MB, but only Test has Ximg and Ypdf  

[ -d "$opath" ] || mkdir -p $opath
outfile=${opath}/css.${nangles}x${nenergies}.h5
python3 ${HOME}/CookieSimSlim/src/run_simulation.py -ofname ${outfile} -n_threads ${nthreads} -offset_threads ${offset} -n_angles ${nangles} -n_energies ${nenergies} -n_images ${nimages} -centralenergy 160 -centralenergyvar 100 -kickstrength 64 -polstrength 1 -polstrengthvar 0
