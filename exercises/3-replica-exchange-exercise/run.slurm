#!/bin/bash

#SBATCH --job-name=lammps_remd
#SBATCH --nodes=1
#SBATCH --tasks-per-node=10
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00

#SBATCH --account=ta132
#SBATCH --partition=standard
#SBATCH --qos=short

module load lammps/15Dec2023

export OMP_NUM_THREADS=1
export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK

srun --distribution=block:block --hint=nomultithread lmp -in run.in -partition 10x1
