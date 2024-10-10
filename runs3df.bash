#!/usr/bin/bash

source /sdf/group/lcls/ds/ana/sw/conda2/manage/bin/psconda.sh

opath=/lscratch/CookieSimSlim_data/
spath=/sdf/scratch/coffee/CookieSimSlim_data/
nthreads=8
nangles=16
nenergies=128
nimages=4096

# 16 angles, 128 energies, 4096 images, less than a minute to run
# and each thread/file is only 77MB, so the whole move at the end is less than 1GB

[ -d "$opath" ] || mkdir -p $opath
outfile=${opath}/css.${nangles}x${nenergies}.h5
#CookieSimSlim/src/run_simulation.py -ofname /mnt/islands/CookieSimSlim_data/css.16x128.h5 -n_threads 4 -n_angles 16 -n_energies 128 -n_images 1024 -centralenergy 64 -centralenergyvar 32 -kickstrength 32 -polstrength 1 -polstrengthvar 0 -offset_threads 0
python3 ${HOME}/CookieSimSlim/src/run_simulation.py -ofname ${outfile} -n_threads ${nthreads} -n_angles ${nangles} -n_energies ${nenergies} -n_images ${nimages} -centralenergy 64 -centralenergyvar 32 -kickstrength 32 -polstrength 1 -polstrengthvar 0
wait
[ -d "$spath" ] || mkdir -p $spath
mv ${opath}/css.* ${spath}
