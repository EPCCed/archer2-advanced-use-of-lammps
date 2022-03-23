#!/bin/bash

#SBATCH --job-name=lammps_rerun
#SBATCH --nodes=1
#SBATCH --tasks-per-node=10
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00

# Replace [budget code] below with your project code (e.g. t01)
#SBATCH --account=[budget code]
#SBATCH --partition=standard
#SBATCH --qos=short

module purge
module load PrgEnv-gnu
module load cray-fftw
module list


srun --distribution=block:block --hint=nomultithread ../lmp_archer2 -in rerun.in -partition 10x1

