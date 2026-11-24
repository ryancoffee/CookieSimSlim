#!/usr/bin/bash

#opath=/media/coffee/9C33-6BBD/CookieSimSlim_tokens
opath=/nvme0/CookieSimSlim_data
nthreads=4
offset=0
nangles=16
nenergies=320
centralen=160
centralenvar=60
kickstrength=100
nimages=1024

# 16 angles, 320 energies (let them mean 1/3 eV per bin), 1024 images, less than a minute to run
# and each thread/file is only 77MB, so the whole move at the end is less than 1GB

[ -d "$opath" ] || mkdir -p $opath
outfile=${opath}/css.${nangles}x${nenergies}.h5
python3 ${HOME}/projects/CookieSimSlim/src/run_simulation.py -ofname ${outfile} -n_threads ${nthreads} -offset_threads ${offset} -n_angles ${nangles} -n_energies ${nenergies} -n_images ${nimages} -centralenergy ${centralen} -centralenergyvar ${centralenvar} -kickstrength ${kickstrength} -polstrength 1 -polstrengthvar 0
