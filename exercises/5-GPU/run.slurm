#!/bin/bash

#SBATCH --job-name=lmp_bench
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --time=0:20:0
#SBATCH --exclusive

#SBATCH --account=ta132
#SBATCH --partition=gpu
#SBATCH --qos=short

module load lammps/8Feb2023-gcc8-impi-cuda118

export OMP_NUM_THREADS=1

# Change --gres=gpu:X above as well
PARAMS="--ntasks=10 --hint=nomultithread --cpus-per-task=1"
srun ${PARAMS} lmp -pk gpu 1 -sf gpu -in in.ethanol -l log.out_${SLURM_TASKS_PER_NODE}

#PARAMS="--ntasks=20 --hint=nomultithread --cpus-per-task=1"
#srun ${PARAMS} lmp -pk gpu 2 -sf gpu -in in.ethanol -l log.out_${SLURM_TASKS_PER_NODE}

#PARAMS="--ntasks=40 --hint=nomultithread --cpus-per-task=1"
#srun ${PARAMS} lmp -pk gpu 4 -sf gpu -in in.ethanol -l log.out_${SLURM_TASKS_PER_NODE}
