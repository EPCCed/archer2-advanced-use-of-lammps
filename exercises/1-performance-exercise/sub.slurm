#!/bin/bash

#SBATCH --job-name=lmp_py
#SBATCH --nodes=1
#SBATCH --time=0:20:0

#SBATCH --account=ta058
#SBATCH --partition=standard
#SBATCH --qos=short

module load PrgEnv-gnu
module load cray-python

export LAMMPS_DIR=/work/ta058/shared/lammps_build
export PATH=${PATH}:${LAMMPS_DIR}/bin
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${LAMMPS_DIR}/lib64
export PYTHONPATH=${PYTHONPATH}:${LAMMPS_DIR}/lib/python3.8/site-packages

export OMP_NUM_THREADS=1

srun -n 1 --cpus-per-task=1 lmp -i in.ethanol -l log.out 
