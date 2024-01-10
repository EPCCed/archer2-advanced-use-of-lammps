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

For this course, we will be using a version of LAMMPS that has been built with the "Python" package and with shared libraries.
These will help us ensure that we can run LAMMPS through Python.

The build instructions used can be found in the
[hpc-uk github](https://github.com/hpc-uk/build-instructions/blob/main/apps/LAMMPS/ARCHER2_2023-12-15_cpe2212.md)
and were:

```bash
module load cpe/22.12
module load cray-fftw/3.3.10.3
module load cmake/3.21.3
module load eigen/3.4.0
module load cray-python

export LD_LIBRARY_PATH=$CRAY_LD_LIBRARY_PATH:$LD_LIBRARY_PATH

# create and source a virtual environment
python -m venv --system-site-packages  /work/y07/shared/apps/core/lammps/15_Dec_2023/venv/lammps-python-15-Dec-2023
source /work/y07/shared/apps/core/lammps/15_Dec_2023/venv/lammps-python-15-Dec-2023/bin/activate

cd lammps-2023-12-15 && mkdir build_cpe && cd build_cpe

cmake -C ../cmake/presets/most.cmake                                       \
      -D BUILD_MPI=on                                                      \
      -D BUILD_SHARED_LIBS=yes                                             \
      -D CMAKE_CXX_COMPILER=CC                                             \
      -D CMAKE_CXX_FLAGS="-O2"                                             \
      -D CMAKE_INSTALL_PREFIX=/work/y07/shared/apps/core/lammps/15Dec2023  \
      -D Eigen3_DIR=/work/y07/shared/libs/core/eigen/3.4.0/include         \
      -D FFT=FFTW3                                                         \
      -D FFTW3_INCLUDE_DIR=${FFTW_INC}                                     \
      -D FFTW3_LIBRARY=${FFTW_DIR}/libfftw3_mpi.so                         \
      -D PKG_MPIIO=yes                                                     \
      ../cmake/

make -j 8
make install
make install-python
```

Of note here:

  - `-D CMAKE_INSTALL_PREFIX=/path/to/install` defines the path into which your LAMMPS executables and libraries will be built.
    You will need to change `/path/to/install` to whatever you like.
  - `-D BUILD_SHARED_LIBS=yes` will build the shared LAMMPS library required to run LAMMPS in Python.
  - `-D PKG_PYTHON=yes` will build the Python packages.
  - The `-C ../cmake/presets/most.cmake` command adds the packages that we are installing.
    Not all of them are required for this course, but it includes all packages that don't need extra libraries.
  - The rest of the instructions are to ensure that the correct compiler is used,
    the MPI version of LAMMPS is built,
    and that it has access to the correct fast Fourier transform (FFTW) and Eigen3 libraries.

Once this is built, you should be able to run LAMMPS from the compute nodes by loading the appropriate module.


## Running LAMMPS through Python

Running LAMMPS through Python is quite a simple task: you can import the LAMMPS Python library, start the LAMMPS environment, and run a LAMMPS simulation by running the following commands:

```python
from lammps import lammps

def main():
    lmp = lammps()
    lmp.file("in.lj")

if __name__ == '__main__':
    main()
```

Python will use the shared LAMMPS libraries to run this.
Under the hood, LAMMPS runs the same processes as it would if the script was run directly through the LAMMPS executable, and jobs run with Python will run in comparable times.

One of the main advantages of running LAMMPS through Python is that it allows  you to make use of Python's dynamic programming.
Also, while LAMMPS offers a large amount of options for writing scripts (via e.g. `variables` definition, `jump` commands and `if` statements), these are not as intuitive to a lot of users as a Python interface.

### Exercise

For this course, we have prepared a number of exercises.
If you have not already done so, you can get a copy of these exercises by running (make sure to run this from `/work`):

```bash
svn checkout https://github.com/EPCCed/archer2-advanced-use-of-lammps/trunk/exercises
```

Once this is downloaded, please `cd exercises/4-python/`.
In this  directory you will find three files:

  - `in.lj` is a LAMMPS input script to simulate a small Lennard-Jones gas.
  - `lammps_lj.py` is a Python script that initially runs the simulation defined in the `in.lj` LAMMPS configuration file.
    Once that is complete, the script will launch a series of simulations run with increasing particle radius.
  - `run.slurm` is the Slurm submission script for running this simulation on the ARCHER2 compute nodes.

You can submit this simulation to the queue by running:

```bash
sbatch run.slurm
```

> ## Changing temperature
> 
> Can you alter the `lammps_lj.py` script to run a set of simulation
> where the temperature of the system is increased by 25 K each step in the series instead of increasing the particle radius?
{: .challenge}

One disadvantage of using the LAMMPS python module is that debugging can be more complicated when things go wrong.
There are more moving parts than with the LAMMPS executable,
and it can often be difficult to trace back errors and attribute them correctly to LAMMPS, Python, or the interface.

> ## Note
> 
> The LAMMPS python module has a number of other features and variables that can be called to improve your use of LAMMPS through Python.
> You can find more information about this in the [LAMMPS manual](https://docs.lammps.org/Python_module.html).
{: .callout}

{% include links.md %}
