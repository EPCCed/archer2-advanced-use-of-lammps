#!/bin/bash

#SBATCH --job-name=lmp_rerun
#SBATCH --nodes=1
#SBATCH --tasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --time=0:20:0

#SBATCH --account=ta132
#SBATCH --partition=standard
#SBATCH --qos=short

module load lammps/15Dec2023

export OMP_NUM_THREADS=1
export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK

srun --distribution=block:block --hint=nomultithread lmp -in in.lj_start -l log.out
#srun --distribution=block:block --hint=nomultithread lmp -in in.lj_rerun -l log_rerun.out
