#!/bin/bash

#SBATCH --job-name=lmp_py
#SBATCH --nodes=1
#SBATCH --time=0:5:0

#SBATCH --account=ta132
#SBATCH --partition=standard
#SBATCH --qos=short
#SBATCH --cpus-per-task=1
#SBATCH --tasks-per-node=128

module load lammps-python/15Dec2023

export OMP_NUM_THREADS=1
export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK

srun --distribution=block:block --hint=nomultithread python lammps_lj.py
