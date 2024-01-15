#!/bin/bash
#SBATCH --partition=lcls
#SBATCH --job-name=lstm
#SBATCH --output=output-%j.txt
#SBATCH --error=output-%j.txt
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=10g
#SBATCH --time=0-20:00:00
#SBATCH --gpus geforce_rtx_2080_ti:0
source ~/.bashrc
conda activate pytorch-gpu
export SLURM_EXACT=1
echo starting run 1 at: `date`
# opath=/sdf/group/lcls/ds/scratch/jhirschm/MRCO_Sim_Data/CookieSimSlim_data/large_even_fiveClass_Dec06_2023_directory/
opath=/sdf/group/lcls/ds/scratch/jhirschm/MRCO_Sim_Data/CookieSimSlim_data/Jan_15_2024_2subPulse/
mkdir -p ${opath}
outfile=${opath}/two_sub_pulse_Jan15_2024.h5
python3 ./src/run_simulation.py -ofname ${outfile} -n_threads 64 -n_images 8192 -n_angles 16 -n_energies 512 -polstrength 1 -polstrengthvar 1 -centralenergy 256 -centralenergyvar 256 -kickstrength 128 -kickstrengthvar 32 -drawscale 4 -custom_single_energy_sase True -selected_centers 2 -max_num_sase 5

# Print the date again -- when finished
echo Finished at: `date`
