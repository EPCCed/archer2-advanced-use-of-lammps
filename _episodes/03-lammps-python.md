---
title: "Using LAMMPS with Python"
teaching: 20
exercises: 25
questions:
- "What does the ARCHER2 software environment look like and how do I access software?"
- "How can I find out what software is available?"
- "How can I request, install or get help with software on ARCHER2?"
objectives:
- "Know how to access different software on ARCHER2 using Lmod modules."
- "Know how to find out what is installed and where to get help."
keypoints:
- "Software is available through modules."
- "The CSE service can help with software issues."
---

## Building LAMMPS with Python

For this course, we will be using a version of LAMMPS that has been built with 
the "Python" package and with shared libraries. These will help us ensure that 
we can run LAMMPS through Python.

The build instructions used were:

```
git clone -b stable https://github.com/lammps/lammps.git mylammps
mkdir mylammps/build; cd mylammps/build

module load PrgEnv-gnu/8.0.0
module load cray-python/3.8.5.0
module load cray-fftw/3.3.8.9
module load cmake/3.21.3

cmake -DCMAKE_CXX_COMPILER=CC \
      -DCMAKE_INSTALL_PREFIX=/work/ta058/shared/lammps_install \
      -DBUILD_MPI=on -D BUILD_SHARED_LIBS=yes \
      -D FFT=FFTW3 -D FFTW3_INCLUDE_DIR=${FFTW_INC} \
      -D FFTW3_LIBRARY=${FFTW_DIR}/libfftw3_mpi.so \
      -D PKG_ASPHERE=yes -D PKG_BODY=yes -D PKG_CLASS2=yes \
      -D PKG_COLLOID=yes -D PKG_COMPRESS=yes -D PKG_CORESHELL=yes \
      -D PKG_DIPOLE=yes -D PKG_GRANULAR=yes -D PKG_MC=yes \
      -D PKG_MISC=yes -D PKG_KSPACE=yes -D PKG_MANYBODY=yes \
      -D PKG_MOLECULE=yes -D PKG_MPIIO=yes -D PKG_OPT=yes \
      -D PKG_PERI=yes -D PKG_QEQ=yes -D PKG_SHOCK=yes -D PKG_OPENMP=yes \
      -D PKG_SRD=yes -D PKG_RIGID=yes -D PKG_REPLICA=yes \
      ../cmake/

make -j 32
make install

```


```
# LAMMPS exports needed
export LAMMPS_DIR=/work/z19/z19/jsindt/LAMMPS_BUILD/mylammps/install
export PATH=${PATH}:${LAMMPS_DIR}/bin
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${LAMMPS_DIR}/lib64
export PYTHONPATH=${PYTHONPATH}:${LAMMPS_DIR}/lib/python3.9/site-packages
```
