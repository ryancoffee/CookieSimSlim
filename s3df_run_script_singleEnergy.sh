#!/bin/bash
##SBATCH --partition=roma
##SBATCH --account=lcls
#SBATCH --job-name=lstm
#SBATCH --output=output-%j.txt
#SBATCH --error=output-%j.txt
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem-per-cpu=10g
#SBATCH --time=0-10:00:00
#SBATCH --gpus 0
#source ~/.bashrc
source /sdf/group/lcls/ds/tools/conda_envs/jackh_pytorch/bin/activate
conda activate jh_pytorch
#source /sdf/group/lcls/ds/ana/sw/conda2/manage/bin/psconda.sh
#conda activate ps-4.6.1-deep 
export SLURM_EXACT=1
echo starting run 1 at: `date`
# opath=/sdf/group/lcls/ds/scratch/jhirschm/MRCO_Sim_Data/CookieSimSlim_data/large_even_fiveClass_Dec06_2023_directory/
# opath=/sdf/group/lcls/ds/scratch/jhirschm/MRCO_Sim_Data/CookieSimSlim_data/Jan_15_2024_2subPulse/
#opath=/sdf/group/lcls/ds/scratch/jhirschm/MRCO_Sim_Data/CookieSimSlim_data/Mar_26_2024_2pulse/
#opath=/sdf/scratch/users/j/jhirschm/CookieSimSlimData/1-Pulse_03282024/
opath=/sdf/data/lcls/ds/prj/prjs2e21/results/2-Pulse_04232024/
#opath=/sdf/home/j/jhirschm/Test
mkdir -p ${opath}
outfile=${opath}/2-Pulse_04232024_File.h5
# python3 ./src/run_simulation.py -ofname ${outfile} -n_threads 64 -n_images 8192 -n_angles 16 -n_energies 512 -polstrength 1 -polstrengthvar 1 -centralenergy 256 -centralenergyvar 256 -kickstrength 128 -kickstrengthvar 32 -drawscale 4 -custom_single_energy_sase True -selected_centers 2 -max_num_sase 5
python3 ./src/run_simulation.py -ofname ${outfile} -n_threads 64 -n_images 8192 -n_angles 16 -n_energies 512 -polstrength 1 -polstrengthvar 1 -centralenergy 256 -centralenergyvar 32 -kickstrength 128 -kickstrengthvar 32 -drawscale 4 -custom_single_energy_sase True -selected_centers 2 -max_num_sase 3

# Print the date again -- when finished
echo Finished at: `date`
