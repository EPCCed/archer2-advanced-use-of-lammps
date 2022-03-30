---
title: "Post-run analysis"
teaching: 15
exercises: 15
questions:
- "How do I write job submission scripts?"
- "How do I control jobs?"
- "How do I find out what resources are available?"
objectives:
- "Understand the use of the basic Slurm commands."
- "Know what components make up and ARCHER2 scheduler."
- "Know where to look for further help on the scheduler."
keypoints:
- "ARCHER2 uses the Slurm scheduler."
- "`srun` is used to launch parallel executables in batch job submission scripts."
- "There are a number of different partitions (queues) available."
---

ARCHER2 uses the Slurm job submission system, or *scheduler*, to manage resources and how they are made
available to users. The main commands you will use with Slurm on ARCHER2 are:

* `sinfo`: Query the current state of nodes
* `sbatch`: Submit non-interactive (batch) jobs to the scheduler
* `squeue`: List jobs in the queue
* `scancel`: Cancel a job
* `salloc`: Submit interactive jobs to the scheduler
* `srun`: Used within a batch job script or interactive job session to start a parallel program

Full documentation on Slurm on ARCHER2 can be found in the [Running Jobs on ARCHER2](https://docs.archer2.ac.uk/user-guide/scheduler/) section of the ARCHER2 documentations.

## Finding out what resources are available: `sinfo`

The `sinfo` command shows the current state of the compute nodes known to the scheduler:

```
auser@uan01:~> sinfo
```
{: .language-bash}
```
PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
standard     up 1-00:00:00    231  alloc nid[001001,001005,001010-001015,001018-001020,001022-001028,001034-001044,001048-001049,001051-001060,001062-001067,001071-001072,001075-001091,001093-001108,001110,001112,001115-001124,001139-001143,001150-001153,001155-001158,001161-001162,001164-001169,001200-001202,001246-001249,001256-001261,001319-001325,001327-001333,001348-001349,001367-001368,001463-001467,001469-001474,001540-001545,001547-001551,001646,001648-001651,001665-001668,001710-001718,001720-001721,001724-001728,001748-001750,001756,001818-001824,001826-001831,001920-001931,001945-001949,001951-001954] 
standard     up 1-00:00:00    669   idle nid[001000,001002-001004,001007-001009,001030-001032,001073,001126-001137,001145-001148,001154,001170,001175-001199,001204-001226,001229-001240,001245,001263-001272,001274-001286,001288-001317,001334-001335,001337-001346,001352-001365,001370-001383,001396-001434,001436-001461,001475-001477,001479-001489,001491-001504,001506-001519,001522-001538,001553-001580,001582-001613,001615-001641,001653-001663,001670-001688,001690-001708,001730-001746,001752-001755,001758-001781,001783-001809,001832,001840-001890,001893-001902,001904-001918,001933-001943,001956-001968,001970-002013,002015-002023] 
```
{: .output}

There is a row for each node state and partition combination. The default output shows the following columns:

* `PARTITION` - The system partition
* `AVAIL` - The status of the partition - `up` in normal operation
* `TIMELIMIT` - Maximum runtime as `days-hours:minutes:seconds`: on ARCHER2, these are set using *QoS*
  (Quality of Service) rather than on partitions
* `NODES` - The number of nodes in the partition/state combination
* `STATE` - The state of the listed nodes (more information below)
* `NODELIST` - A list of the nodes in the partition/state combination

The nodes can be in many different states, the most common you will see are:

* `idle` - Nodes that are not currently allocated to jobs
* `alloc` - Nodes currently allocated to jobs
* `draining` - Nodes draining and will not run further jobs until released by the systems team
* `down` - Node unavailable
* `fail` - Node is in fail state and not available for jobs
* `reserved` - Node is in an advanced reservation and is not generally available
* `maint` - Node is in a maintenance reservation and is not generally available

If you prefer to see the state of individual nodes, you can use the `sinfo -N -l` command.

> ## Lots to look at!
> Warning! The `sinfo -N -l` command will produce a lot of output as there are over 5000 individual 
> nodes on ARCHER2!
{: .callout}

```
auser@uan01:~> sinfo -N -l
```
{: .language-bash}
```
Thu Oct 29 21:22:08 2020
NODELIST   NODES PARTITION       STATE CPUS    S:C:T MEMORY TMP_DISK WEIGHT AVAIL_FE REASON               
nid001000      1  standard        idle 256    2:64:2 256000        0      1   (null) none                 
nid001001      1  standard   allocated 256    2:64:2 256000        0      1   (null) none                 
nid001002      1  standard        idle 256    2:64:2 256000        0      1   (null) none                 
nid001003      1  standard        idle 256    2:64:2 256000        0      1   (null) none                 
nid001004      1  standard        idle 256    2:64:2 256000        0      1   (null) none                 
nid001005      1  standard   allocated 256    2:64:2 256000        0      1   (null) none                 
nid001006      1  standard       down* 256    2:64:2 256000        0      1   (null) Not responding       
nid001007      1  standard        idle 256    2:64:2 256000        0      1   (null) none                 
nid001008      1  standard        idle 256    2:64:2 256000        0      1   (null) none                 
nid001009      1  standard        idle 256    2:64:2 256000        0      1   (null) none                 
nid001010      1  standard   allocated 256    2:64:2 256000        0      1   (null) none                 
nid001011      1  standard   allocated 256    2:64:2 256000        0      1   (null) none                 
nid001012      1  standard   allocated 256    2:64:2 256000        0      1   (null) none                 
nid001013      1  standard   allocated 256    2:64:2 256000        0      1   (null) none                 
nid001014      1  standard   allocated 256    2:64:2 256000        0      1   (null) none                 
nid001015      1  standard   allocated 256    2:64:2 256000        0      1   (null) none                 
...lots of output trimmed...

```
{: .output}

> ## Explore a compute node
> Let’s look at the resources available on the compute nodes where your jobs will actually run. Try running this
> command to see the name, CPUs and memory available on the worker nodes (the instructors will give you the ID of
> the compute node to use):
> ```
> [auser@uan01:~> sinfo -n nid001000 -o "%n %c %m"
> ```
> {: .language-bash}
> This should display the resources available for a standard node. Can you use `sinfo` to find out the range of
> node IDs for the high memory nodes?
> > ## Solution
> > The high memory nodes have IDs `nid000001-nid000004`. You can get this by using:
> >
> > ```
> > auser@uan01:~> sinfo -N -l -S "-m" | less
> > ```
> > {: .language-bash}
> >
> > The `-S "-m"` option tells `sinfo` to print the node list sorted by decreasing memory per node. This
> > output is then piped into `less` so we can examine the output a page at a time without it scrolling
> > off the screen.
> >
> {: .solution}
{: .challenge}

## Using batch job submission scripts

### Header section: `#SBATCH`

As for most other scheduler systems, job submission scripts in Slurm consist of a header section with the
shell specification and options to the submission command (`sbatch` in this case) followed by the body of
the script that actually runs the commands you want. In the header section, options to `sbatch` should 
be prepended with `#SBATCH`.

Here is a simple example script that runs the `xthi` program, which shows process and thread placement, across
two nodes.

```
#!/bin/bash
#SBATCH --job-name=my_mpi_job
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --time=0:10:0
#SBATCH --account=ta016
#SBATCH --partition=standard
#SBATCH --qos=standard

# This will restore the appropriate programming environment
# (in this case, the GNU PE)
module load epcc-job-env

# Now load the "xthi" package
module load xthi

export OMP_NUM_THREADS=1

# Load modules, etc.
# srun to launch the executable
srun --distribution=block:block --hint=nomultithread xthi
```
{: .language-bash}

The options shown here are:

* `--job-name=my_mpi_job` - Set the name for the job that will be displayed in Slurm output
* `--nodes=2` - Select two nodes for this job
* `--ntasks-per-node=128` - Set 128 parallel processes per node (usually corresponds to MPI ranks)
* `--cpus-per-task=1` - Number of cores to allocate per parallel process 
* `--time=0:10:0` - Set 10 minutes maximum walltime for this job
* `--account=ta016` - Charge the job to the `ta016` budget

We will discuss the `srun` command further below.

### Submitting jobs using `sbatch`

You use the `sbatch` command to submit job submission scripts to the scheduler. For example, if the
above script was saved in a file called `test_job.slurm`, you would submit it with:

```
auser@uan01:~> sbatch test_job.slurm
```
{: .language-bash}
```
Submitted batch job 23996
```
{: .output}

Slurm reports back with the job ID for the job you have submitted

> ## What are the default for `sbatch` options?
> If you do not specify job options, what are the defaults for Slurm on ARCHER2? Submit jobs to find out
> what the defaults are for:
> 
> 1. Budget (or Account) the job is charged to?
> 2. Tasks per node?
> 3. Number of nodes?
> 4. Walltime? (This one is hard!)
> 
> > ## Solution
> > 
> > You can get the answers to 1., 2., and 3. with the following script:
> > 
> > ```
> > #!/bin/bash
> > #SBATCH --job-name=my_mpi_job
> > module load epcc-job-env
> > 
> > echo "Nodes: $SLURM_JOB_NUM_NODES"
> > echo "Tasks per node: $SLURM_NTASKS_PER_NODE"
> > module load xthi
> > 
> > export OMP_NUM_THREADS=1
> > 
> > srun --distribution=block:block --hint=nomultithread xthi
> > ```
> > {: .language-bash}
> > 
> > (1) Budget: It depends. In most cases, you will have a default budget to 
> > which jobs will be charged. This is not always the case, though.
> > 
> > (2) Tasks per node: 256
> >
> > (3) Number of nodes: 1
> >
> > (4) Getting the default time limit is more difficult - we need to use 
> > `sacct` to query the time limit set for the job. For example, if the job 
> > ID was "12345", then we could query the time limit with:
> > 
> > ```
> > auser@uan01:~> sacct -o "TimeLimit" -j 12345
> > ```
> > {: .language-bash}
> > ```
> >  Timelimit 
> > ---------- 
> >  00:10:00 
> > ```
> > {: .output}
> >
> {: .solution}
{: .challenge}

### Checking progress of your job with `squeue`

You use the `squeue` command to show the current state of the queues on ARCHER2. Without any options, it
will show all jobs in the queue:

```
auser@uan01:~> squeue
```
{: .language-bash}
```
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
```
{: .output}

### Cancelling jobs with `scancel`

You can use the `scancel` command to cancel jobs that are queued or running. When used on running jobs
it stops them immediately.

> ## Getting notified
> Slurm on ARCHER2 can also send e-mails to notify you when your job starts, ends, fails, etc. Can
> you find out how you would setup your job script to send you an e-mail when your job finishes and
> when it fails? Test your answer, does it work?
> > ## Solution
> > The option `--mail-type=END,FAIL` will send mailings to you when the job ends or fails. You can
> > also use the event `TIME_LIMIT` to notify you if a job reaches its walltime without finishing and
> > the events `TIME_LIMIT_50`, `TIME_LIMIT_80` and `TIME_LIMIT_90` to notify you when your job is
> > 50%, 80% and 90% of the way through the specified walltime.
> {: .solution}
{: .challenge}

### Running parallel applications using `srun`

Once past the header section your script consists of standard shell commands required to run your
job. These can be simple or complex depending on how you run your jobs but even the simplest job
script usually contains commands to:

* Load the required software modules
* Set appropriate environment variables (you should always set `OMP_NUM_THREADS`, even if you are
  not using OpenMP you should set this to `1`)

After this you will usually launch your parallel program using the `srun` command. At its simplest,
`srun` only needs 1 argument to specify the correct binding of processes to cores (it will use the
values supplied to `sbatch` to work out how many parallel processes to launch). In the example above,
our `srun` command simply looks like:

```
srun --distribution=block:block --hint=nomultithread xthi
```
{: .language-bash}

> ## Underpopulation of nodes
> You may often want to *underpopulate* nodes on ARCHER2 to access more memory or more memory 
> bandwidth per task. Can you state the `sbatch` options you would use to run `xthi`:
> 
> 1. On 4 nodes with 64 tasks per node?
> 2. On 8 nodes with 2 tasks per node, 1 task per socket?
> 3. On 4 nodes with 32 tasks per node, ensuring an even distribution across the 8 NUMA regions
> on the node?
> 
> Once you have your answers run them in job scripts and check that the binding of tasks to 
> nodes and cores output by `xthi` is what you expect.
> 
> > ## Solution
> > 1. `--nodes=4 --ntasks-per-node=64`
> > 2. `--nodes=8 --ntasks-per-node=2 --ntasks-per-socket=1`
> > 3. `--nodes=4 --ntasks-per-node=32 --ntasks-per-socket=16 --cpus-per-task=4`
> {: .solution}
{: .challenge}

### Hybrid MPI and OpenMP jobs

When running hybrid MPI (with the individual tasks also known as ranks or processes) and OpenMP
(with multiple threads) jobs you need to leave free cores between the parallel tasks launched
using `srun` for the multiple OpenMP threads that will be associated with each MPI task.

As we saw above, you can use the options to `sbatch` to control how many parallel tasks are
placed on each compute node and can use the `--cpus-per-task` option to set the stride 
between parallel tasks to the right value to accommodate the OpenMP threads - the value
for `--cpus-per-task` should usually be the same as that for `OMP_NUM_THREADS`. To ensure
you get the correct thread pinning, you also need to specify an additional OpenMP environment
variable and a couple of additional options to `srun`. Specifically:

   - Set the `OMP_PLACES` environment variable to `cores` with `export OMP_PLACES=cores` in 
     you job submission script
   - Add the `--hint=nomultithread` option to `srun`
   - Add the `--distribution=block:block` option to `srun`

As an example, consider the job script below that runs across 2 nodes with 8 MPI tasks
per node and 16 OpenMP threads per MPI task (so all 256 cores across both nodes are used).

```
#!/bin/bash
#SBATCH --job-name=my_hybrid_job
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=16
#SBATCH --time=0:10:0
#SBATCH --account=ta016
#SBATCH --partition=standard
#SBATCH --qos=standard

# This will restore the appropriate programming environment
# (in this case, the GNU PE)
module load epcc-job-env

# Now load the "xthi" package
module load xthi

export OMP_NUM_THREADS=16
export OMP_PLACES=cores

# Load modules, etc.
# srun to launch the executable
srun --hint=nomultithread --distribution=block:block xthi
```
{: .language-bash}

Each ARCHER2 compute node is made up of 8 NUMA (*Non Uniform Memory Access*) regions (4 per socket) 
with 16 cores in each region. Programs where the threads of a task span multiple NUMA regions
are likely to be *less* efficient so we recommend using thread counts that fit well into the
ARCHER2 compute node layout. Effectively, this means one of the following options for nodes
where all cores are used:

* 8 MPI tasks per node and 16 OpenMP threads per task: equivalent to 1 MPI task per NUMA region
* 16 MPI tasks per node and 8 OpenMP threads per task: equivalent to 2 MPI tasks per NUMA region
* 32 MPI tasks per node and 4 OpenMP threads per task: equivalent to 4 MPI tasks per NUMA region
* 64 MPI tasks per node and 2 OpenMP threads per task: equivalent to 8 MPI tasks per NUMA region 

## STDOUT/STDERR from jobs

STDOUT and STDERR from jobs are, by default, written to a file called `slurm-<jobid>.out` in the
working directory for the job (unless the job script changes this, this will be the directory
where you submitted the job). So for a job with ID `12345` STDOUT and STDERR would be in
`slurm-12345.out`.

If you run into issues with your jobs, the Service Desk will often ask you to send your job
submission script and the contents of this file to help debug the issue.

If you need to change the location of STDOUT and STDERR you can use the `--output=<filename>`
and the `--error=<filename>` options to `sbatch` to split the streams and output to the named
locations.

## Other useful information

In this section we briefly introduce other scheduler topics that may be useful to users. We
provide links to more information on these areas for people who may want to explore these 
areas more. 

### Interactive jobs: direct `srun` 

Similar to the batch jobs covered above, users can also run interactive jobs using the `srun`
command directly. `srun` used in this way takes the same arguments as `sbatch` but, obviously, these are 
specified on the command line rather than in a job submission script. As for `srun` within 
a batch job, you should also provide the name of the executable you want to run.

For example, to execute `xthi` across all cores on two nodes (1 MPI task per core and no
OpenMP threading) within an interactive job you would issue the following commands:

```
auser@uan01:~> srun --partition=standard --qos=standard --nodes=2 --ntasks-per-node=128 --cpus-per-task=1 --time=0:10:0 --account=ta016 xthi
```
{: .language-bash}
```
Node    0, hostname nid001030
Node    1, hostname nid001031
Node    0, rank    0, thread   0, (affinity = 0,128)
Node    0, rank    1, thread   0, (affinity = 16,144)
Node    0, rank    2, thread   0, (affinity = 32,160)
Node    0, rank    3, thread   0, (affinity = 48,176)
Node    0, rank    4, thread   0, (affinity = 64,192)
Node    0, rank    5, thread   0, (affinity = 80,208)
Node    0, rank    6, thread   0, (affinity = 96,224)
Node    0, rank    7, thread   0, (affinity = 112,240)
Node    0, rank    8, thread   0, (affinity = 1,129)
Node    0, rank    9, thread   0, (affinity = 17,145)
Node    0, rank   10, thread   0, (affinity = 33,161)
Node    0, rank   11, thread   0, (affinity = 49,177)
Node    0, rank   12, thread   0, (affinity = 65,193)
Node    0, rank   13, thread   0, (affinity = 81,209)
Node    0, rank   14, thread   0, (affinity = 97,225)
...long output trimmed...
```
{: .output}


<!-- Need to add information on the solid state storage and Slurm once it is in place

### Using the ARCHER2 solid state storage

-->


{% include links.md %}
