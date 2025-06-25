#!/bin/bash
#SBATCH --account=lcls
#SBATCH --partition=milano
#SBATCH --job-name=tofs
#SBATCH --output=output-%j.txt
#SBATCH --error=output-%j.txt
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=20g
#SBATCH --time=0-1:00:00

source /sdf/group/lcls/ds/tools/conda_envs/jackh_pytorch/bin/activate
conda deactivate
conda activate jh_pytorch
opath=/sdf/home/j/jhirschm/Test
mkdir -p ${opath}
outfile=${opath}/test_file.h5
python3 tester.py
#source /sdf/group/lcls/ds/ana/sw/conda2/manage/bin/psconda.sh
#conda deactivate
#conda activate tf-gpu

echo finished
