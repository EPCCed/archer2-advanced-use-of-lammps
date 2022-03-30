---
title: "Compiling LAMMPS and using it with Python"
teaching: 20
exercises: 25
questions:
- "How can I compile LAMMPS using CMake"
- "How do I build LAMMPS with its shared libraries?"
- "How can I run LAMMPS from within Python?"
objectives:
- "Know how to compile LAMMPS on ARCHER2 (and what to look for when compiling 
  elsewhere."
- "Know how run a LAMMPS simulation through Python."
keypoints:
- "Compiling LAMMPS with CMake is easy and quick on ARCHER2"
- "Running LAMMPS through Python can have certain advantages."
- "However, finding the root cause of problems when things go wrong is harder 
  to do when running LAMMPS through Python rather than through a LAMMPS 
  executable."
---

## Building LAMMPS with Python

For this course, we will be using a version of LAMMPS that has been built with 
the "Python" package and with shared libraries. These will help us ensure that 
we can run LAMMPS through Python.

The build instructions used were:

```bash
git clone -b stable https://github.com/lammps/lammps.git mylammps
mkdir mylammps/build; cd mylammps/build

module load PrgEnv-gnu/8.0.0
module load cray-python/3.8.5.0
module load cray-fftw/3.3.8.9
module load cmake/3.21.3

cmake -DCMAKE_CXX_COMPILER=CC -DCMAKE_INSTALL_PREFIX=/path/to/install \
      -DBUILD_MPI=on -D BUILD_SHARED_LIBS=yes -D FFT=FFTW3 \
      -D FFTW3_INCLUDE_DIR=/opt/cray/pe/fftw/3.3.8.9/x86_rome/include \
      -D FFTW3_LIBRARY=/opt/cray/pe/fftw/3.3.8.9/x86_rome/lib/libfftw3_mpi.so \
      -D PKG_ASPHERE=yes -D PKG_BODY=yes -D PKG_CLASS2=yes -D PKG_COLLOID=yes \
      -D PKG_COMPRESS=yes -D PKG_CORESHELL=yes -D PKG_DIPOLE=yes \
      -D PKG_GRANULAR=yes -D PKG_MC=yes -D PKG_MISC=yes -D PKG_KSPACE=yes \
      -D PKG_MANYBODY=yes -D PKG_MOLECULE=yes -D PKG_MPIIO=yes \
      -D PKG_OPENMP=yes -D PKG_OPT=yes -D PKG_PERI=yes -D PKG_PYTHON=yes \
      -D PKG_QEQ=yes -D PKG_SHOCK=yes -D PKG_SRD=yes -D PKG_RIGID=yes \
      -D PKG_REPLICA=yes \
      ../cmake/

make -j 8
make install
```
Of note here:

  - `-DCMAKE_INSTALL_PREFIX=/path/to/install` defines the path into which your 
    LAMMPS executables and libraries will be built. You will need to change 
    `/path/to/install` to whatever you like.
  - `-D BUILD_SHARED_LIBS=yes` will build the shared LAMMPS library required 
    to run LAMMPS in Python.
  - `-D PKG_PYTHON=yes` will build the Python packages.
  - The `-D PKG_<package_name>` commands name the packages that we are 
    installing. Not all of them are required for this course.
  - The rest of the instructions are to ensure that the MPI version of LAMMPS 
    is built, and that it has access to the correct fast Fourier transform 
    (FFTW) libraries.

Once this is built, you should be able to run LAMMPS from the compute nodes by 
loading the appropriate modules and setting the `PATH`, `LD_LIBRARY_PATH`, and 
`PYTHONPATH` variables to point to the appropriate LAMMPS directories. (As an 
aside, this is effectively what modulefiles do -- when you load a module, the 
modulefile will first load any dependent modules and then add the required 
paths to your path variables.)


```bash
module load PrgEnv-gnu/8.0.0
module load cray-python/3.8.5.0

# LAMMPS exports needed
export LAMMPS_DIR=/path/to/install
export PATH=${PATH}:${LAMMPS_DIR}/bin
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${LAMMPS_DIR}/lib64
export PYTHONPATH=${PYTHONPATH}:${LAMMPS_DIR}/lib/python3.9/site-packages
```

## Running LAMMPS through Python

Running LAMMPS through Python is quite a simple task: you can import the 
LAMMPS Python library, start the LAMMPS environment, and run a LAMMPS 
simulation by running the following commands:

```python
from lammps import lammps

def main():
    lmp = lammps()
    lmp.file("in.lj")

if __name__ == '__main__':
    main()
```

Python will use the shared LAMMPS libraries to run this. Under the hood, 
LAMMPS runs the same processes as it would if the script was run directly 
through the LAMMPS executable, and jobs run with Python will run in comparable 
times.

One of the main advantages of running LAMMPS through Python is that it allows 
you to make use of Python's dynamic programming. Also, while LAMMPS offers a 
large amount of options for writing scripts (via e.g. `variables` definition, 
`jump` commands and `if` statements), these are not as intuitive to a lot of 
users as a Python interface.

### Exercise

For this course, we have prepared a number of exercises. If you have not 
already done so, you can get a copy of these exercises by running (make 
sure to run this from `/work`):

```bash
svn checkout https://github.com/EPCCed/archer2-advanced-use-of-lammps/trunk/exercises
```

Once this is downloaded, please  `cd exercises/4-python/`. In this 
directory you will find three files:

  - `in.lj` is a LAMMPS input script to simulate a small Lennard-Jones gas.
  - `lammps_lj.py` is a Python script that initially runs the simulation 
    defined in the `in.lj` LAMMPS configuration file. Once that is complete, 
    the script will launch a series of simulations run with increasing 
    particle radius.
  - `sub.slurm` is the Slurm submission script for running this simulation on 
    the ARCHER2 compute nodes.

You can submit this simulation to the queue by running:

```bash
sbatch sub.slurm
```

> ## Changing temperature
> 
> Can you alter the `lammps_lj.py` script to run a set of simulation where the 
> temperature of the system is increased by 25 K each step in the series 
> instead of increasing the particle radius?
> 
{: .challenge}

One disadvantage of using the LAMMPS python module is that debugging can be 
more complicated when things go wrong. There are more moving parts than with 
the LAMMPS executable, and it can often be difficult to trace back errors and 
attribute them correctly to LAMMPS, Python, or the interface.

> ## Note
> 
> The LAMMPS python module has a number of other features and variables that 
> can be called to improve your use of LAMMPS through Python. You can find 
> more information about this in the 
> [LAMMPS manual](https://docs.lammps.org/Python_module.html).
> 
{: .callout}

{% include links.md %}
