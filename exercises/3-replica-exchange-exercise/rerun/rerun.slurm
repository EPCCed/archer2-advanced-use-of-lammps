#!/bin/bash

#SBATCH --job-name=lammps_rerun
#SBATCH --nodes=1
#SBATCH --tasks-per-node=10
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00

#SBATCH --account=z19
#SBATCH --partition=standard
#SBATCH --qos=short

module load lammps/15Dec2023

export OMP_NUM_THREADS=1
export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK

srun --distribution=block:block --hint=nomultithread lmp -in rerun.in -partition 10x1

