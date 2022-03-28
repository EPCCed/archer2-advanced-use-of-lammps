---
title: "Measuring and improving LAMMPS performance"
teaching: 30
exercises: 45
questions:
- "How can we run LAMMPS on ARCHER2?"
- "How can we improve the performance of LAMMPS?"
objectives:
- "Gain an overview of submitting and running jobs on the ARCHER2 service."
- "Gain an overview of methods to improve the performance of LAMMPS."
keypoints:
- "LAMMPS offers a number of built in methods to improve performance."
- "It is important to spend some time understanding your system and 
   considering its performance."
- "Where possible, always run a quick benchmark of your system before setting 
   up a large run."
---

## Running LAMMPS on ARCHER2

ARCHER2 uses a module system. In general, you can run LAMMPS on ARCHER2 by 
using the LAMMPS module:

```bash
ta058js@ln03:~> module avail lammps

------------------- /work/y07/shared/archer2-lmod/apps/core -------------------
   lammps/29_Sep_2021

```

Running `module load lammps` will set up your environment to use LAMMPS. For 
this course, we will be using certain LAMMPS packages that are not included in 
the central module. We have built a version of LAMMPS that can be accessed by 
ensuring that the following commands are run prior to executing your LAMMPS 
command.

```bash
module load PrgEnv-gnu
module load cray-python

export LAMMPS_DIR=/work/z19/z19/jsindt/LAMMPS_BUILD/mylammps/install
export PATH=${PATH}:${LAMMPS_DIR}/bin
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${LAMMPS_DIR}/lib64
export PYTHONPATH=${PYTHONPATH}:${LAMMPS_DIR}/lib/python3.9/site-packages
```

The build instructions for this version are described in the next section of 
the course.

Once your environment is set up, you will have access to the `lmp` LAMMPS 
executable. Note that you will only be able to run this on a single core on 
the ARCHER2 login node.

### Submitting a job to the compute nodes

To run LAMMPS on multiple cores/nodes, you will need to submit a job to the 
ARCHER2 compute nodes. The compute nodes do not have access to the landing 
`home` filesystem -- this filesystem is to store useful/important information. 
On ARCHER2, when submitting jobs to the compute nodes, make sure that you are 
in your `/work/ta058/ta058/<username>` directory.

For this course, we have prepared a number of exercises. You can get a copy of 
these exercises by running (make sure to run this from `/work`):

```bash
svn checkout https://github.com/EPCCed/archer2-advanced-use-of-lammps/trunk/exercises
```

Once this is downloaded, please  `cd exercises/1-performance-exercise/`. In this 
directory you will find three files:

  - `sub.slurm` is a Slurm submission script -- this will let you submit jobs 
    to the compute nodes. Initially, it will run a single core job, but we 
    will be editing it to run on more cores.
  - `in.ethanol` is the LAMMPS input script that we will be using for this 
    exercise. This script is meant to run a small simulation of 125 ethanol 
    molecules in a periodic box.
  - `data.ethanol` is a LAMMPS data file for a single ethanol molecule. This 
    template will be copied by the `in.lammps` file to generate our simulation 
    box.

To submit your first job on ARCHER2, please run:

```bash
sbatch sub.slurm
```

You can check the progress of your job by running `squeue -u ${USER}`. Your 
job state will go from `PD` (pending) to `R` (running) to `CG` (cancelling). 
Once your job is complete, it will have produced a file called 
`slurm-####.out` -- this file contains the STDOUT and STDERR produced by your 
job.

The job will also produce a LAMMPS log file `log.out`. In this file, you will 
find all of the thermodynamic outputs that were specified in the LAMMPS 
`thermo_style`, as well as some very useful performance information! After 
every `run` is complete, LAMMPS outputs a series of information that can be 
used to better understand the behaviour of your job.

```
Loop time of 197.21 on 1 procs for 10000 steps with 1350 atoms

Performance: 4.381 ns/day, 5.478 hours/ns, 50.707 timesteps/s
100.0% CPU use with 1 MPI tasks x 1 OpenMP threads

MPI task timing breakdown:
Section |  min time  |  avg time  |  max time  |%varavg| %total
---------------------------------------------------------------
Pair    | 68.063     | 68.063     | 68.063     |   0.0 | 34.51
Bond    | 5.0557     | 5.0557     | 5.0557     |   0.0 |  2.56
Kspace  | 5.469      | 5.469      | 5.469      |   0.0 |  2.77
Neigh   | 115.22     | 115.22     | 115.22     |   0.0 | 58.43
Comm    | 1.4039     | 1.4039     | 1.4039     |   0.0 |  0.71
Output  | 0.00034833 | 0.00034833 | 0.00034833 |   0.0 |  0.00
Modify  | 1.8581     | 1.8581     | 1.8581     |   0.0 |  0.94
Other   |            | 0.139      |            |       |  0.07

Nlocal:        1350.00 ave        1350 max        1350 min
Histogram: 1 0 0 0 0 0 0 0 0 0
Nghost:        10250.0 ave       10250 max       10250 min
Histogram: 1 0 0 0 0 0 0 0 0 0
Neighs:        528562.0 ave      528562 max      528562 min
Histogram: 1 0 0 0 0 0 0 0 0 0

Total # of neighbors = 528562
Ave neighs/atom = 391.52741
Ave special neighs/atom = 7.3333333
Neighbor list builds = 10000
Dangerous builds not checked
Total wall time: 0:05:34
```

The ultimate aim is always to get your simulation to run in a sensible amount 
of time. This often simply means trying to optimise the final value ("Total 
wall time"), though some people care more about optimising efficiency (wall 
time multiplied by core count). In this lesson, we will be focusing on what 
we can do to improve these.

## Increasing computational resources

The first approach that most people take to increase the speed of their 
simulations is to increase the computational resources. If your system can 
accommodate this, doing this can sometimes lead to "easy" improvements. 
However, this usually comes at an increased cost (if running on a system for 
which compute is charged) and does not always lead to the desired results.

In your first run, LAMMPS was run on a single core. For a large enough system, 
increasing the number of cores used should reduce the total run time. In your 
`sub.slurm` file, you can edit the `-n #` in the line:

```bash
srun --exact -n 1 lmp -i in.ethanol -l log.out
```

to run on more cores. An ARCHER2 node has 128 cores, so you could potential 
run on up to 128 cores.


> ## Quick benchmark
> As a first exercise, fill in the table below.
> |Number of cores| Walltime | Performance (ns/day) |
> |---------------|----------|----------------------|
> |   1  | | | |
> |   2  | | | |
> |   4  | | | |
> |   8  | | | |
> |  16  | | | |
> |  32  | | | |
> |  64  | | | |
> | 128  | | | |
> Do you spot anything unusual in these run times? If so, can you explain this 
> strange result?
> > ## Solution
> > The simulation takes almost the same amount of time when running on a 
> > single core as when running on two cores. A more detailed look into the 
> > `in.ethanol` file will reveal that this is because the simulation box is 
> > not uniformly packed.
> > At the start of the simulation (initial equilibration), the simulation box 
> > looks like this:
> > {% include figure.html url="" max-width="80%" file="/fig/2_performance/start_sim_box.jpg" alt=""Simulation box at the start of the simulation" caption="Simulation box at the start of the simulation" %}
> {: .solution}
{: .challenge}

> ### Note!
> Here are only considering MPI parallelisation -- LAMMPS offers the option 
> to run using joint MPI+OpenMP (more on that later), but for the exercises 
> in this lesson, we will only be considering MPI.
{: .callout}

## Domain decomposition

In the exercise above, you will (hopefully) have noticed that, while the 
simulation run time decreases overall, the jump from 

## Considering neighbour lists

Let's take another look at the profiling information provided by LAMMPS:

```
Section |  min time  |  avg time  |  max time  |%varavg| %total
---------------------------------------------------------------
Pair    | 68.063     | 68.063     | 68.063     |   0.0 | 34.51
Bond    | 5.0557     | 5.0557     | 5.0557     |   0.0 |  2.56
Kspace  | 5.469      | 5.469      | 5.469      |   0.0 |  2.77
Neigh   | 115.22     | 115.22     | 115.22     |   0.0 | 58.43
Comm    | 1.4039     | 1.4039     | 1.4039     |   0.0 |  0.71
Output  | 0.00034833 | 0.00034833 | 0.00034833 |   0.0 |  0.00
Modify  | 1.8581     | 1.8581     | 1.8581     |   0.0 |  0.94
Other   |            | 0.139      |            |       |  0.07
```

This output can provide us with a lot of valuable information about where our 
simulation is taking a long time, and can help us assess where we can save 
time. In the example above, we notice that the majority of the time is spent 
in the `Neigh` section -- e.g. a lot of time is spent calculating neighbour 
lists.



## Further tips

### Shake

### Hybrid MPI+OpenMP runs

- always study the timing summary. there is lots of useful information there. Pair should be dominant. When using KSpace optimum is often to have KSpace take less than 30%, often around 10%, similarly for Neigh.

-  Neigh can be adjusted with cutoff and neighbor list skin and update frequency. To find a good value for neigh_modify delay and every run with delay 0 every 1 check yes and look at the number of neighbor list builds. compute the average and use a delay that is safely less than that and then run with every 1 or 2 and check for dangerous builds. the system needs to be equilibrated. gains from tweaking skin are small unless cutoffs are short.

- When running with GPU package acceleration, it is often better to leave KSpace on the CPU (since its acceleration potential is limited, but it can run concurrently to Pair (which is thus mostly "free" and one may increase the coulomb cutoff unless the time spent on Pair (with acceleration) matches Bond+KSpace.

- For inhomogeneous systems or systems with large vacuum one needs to watch out for load imbalance. LAMMPS decomposes based on volume not density. the largest gain is often from using the processors keyword to adjust the processor grid. then one can consider the balance command, then fix balance and finally switching to tiled communication and decomposition. please see the new LAMMPS paper and/or the manual for some discussion of brick versus tiled.

- MPI and domain decomposition is most of the time the most efficient parallelization. smaller subdomains bring also more cache efficiency, which does not apply to multi-threading. OpenMP should be used when there are many cores on a node so that MPI has bandwidth issues. OpenMP should be limited to a socket. Processor and memory affinity settings are also important (and can produce 10% or so difference in performance).

- People should pay attention to not using too many MPI ranks. that can kill performance. biggest challenge for running large systems with many MPI ranks is KSpace due to having to do global transposes of the grids and - because lammps uses "pencils" - there is effectively only a 2d decomposition possible. Once KSpace becomes significant, it is better to use MPI+OpenMP to reduce the number of MPI ranks for KSpace. an additional option is to use run style verlet/split where a separate partition is assigned to KSpace and the rest can be run with a number of MPI ranks that is an integer multiple of the KSpace ranks.

- a particular pet peeve of mine are people that suffer from "premature optimization", i.e. they worry about efficiency of something that doesn't contribute much before even having figured out how to run their system and also people that run too large systems right  away without knowing anything. good planning is key to successful research with efficient usage of resources. a frequent example are people that equilibrate a bulk liquid to save time for a calculation of a slab system, but then run into issues with image flags and complete disregard that switching from periodic to non-periodic boundaries is a drastic change that usually requires more time and effort to be dissipated and re-equilibrated than what was potentially saved. better to start with non-periodic right away and add a wall fix to contain particles.

- i don't think I have to tell you anything about how important benchmarking, especially scaling to large systems and many mpi ranks is and also how helpful careful profiling can be (the timing summary in LAMMPS is a good start but for particular problems one needs the real deal). on linux machines I have learned a lot from using kernel based profiling with "perf". sometimes just logging into the compute nodes and doing "perf top" can be very instructive. on the other hand, one can easily spend too much time on trying to squeeze the last bit of performance to make a calculation faster. this is often not worth the time. reaching 80% of the optimum can often be reached with 20% effort

{% include links.md %}

