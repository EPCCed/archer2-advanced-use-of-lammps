#!/bin/bash

#SBATCH --job-name=lammps_remd
#SBATCH --nodes=1
#SBATCH --tasks-per-node=10
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00

#SBATCH --account=ta058
#SBATCH --partition=standard
#SBATCH --qos=short

module load PrgEnv-gnu
module load cray-python

export LAMMPS_DIR=/work/ta058/shared/lammps_build
export PATH=${PATH}:${LAMMPS_DIR}/bin
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${LAMMPS_DIR}/lib64
export PYTHONPATH=${PYTHONPATH}:${LAMMPS_DIR}/lib/python3.9/site-packages


srun --distribution=block:block --hint=nomultithread lmp -in run.in -partition 10x1
