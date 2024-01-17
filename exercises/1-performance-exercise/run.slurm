#!/bin/bash

#SBATCH --job-name=lmp_bench
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:20:0

#SBATCH --account=ta132
#SBATCH --partition=standard
#SBATCH --qos=short

module load lammps/15Dec2023

export OMP_NUM_THREADS=1
export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK
	
srun lmp -in in.ethanol -l log.out_${SLURM_TASKS_PER_NODE}
