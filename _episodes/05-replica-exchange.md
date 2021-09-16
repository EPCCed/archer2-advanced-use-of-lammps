---
title: "Replica exchange"
teaching: 20
exercises: 10
questions:
- "How can I be a responsible user?"
- "How can I protect my data?"
objectives:
- "Learn how to be a considerate shared system citizen."
- "Understand how to protect your critical data."
keypoints:
- "Be careful how you use the login node."
- "Your data on the system is your responsibility."
- "Again, don't run stuff on the login node."
- "Don't be a bad person and run stuff on the login node."
---

## What can I do on the login nodes? What shouldn't I do?

The login node is often very busy managing lots of users logged in, creating and editing files
and compiling software. It does not have any extra space to run computational work and you will
get poor performance if you try to use it for computational work.

Do not run jobs on the login node (though quick tests are generally fine). A “quick test” is
generally anything that uses less than 5 minutes of time. If you
use too much resource then other users on the login node may start to be affected - their
login sessions will start to run slowly and may even freeze or hang. 

> ## Login nodes are a shared resource
>
> Remember, the login node is shared with all other users and your actions could cause
> issues for other people. Think carefully about the potential implications of issuing
> commands that may use large amounts of resource.
>
{: .callout}

You can always use the command `ps ux` to list the processes you are running on a login
node and the amount of CPU and memory they are using. The `kill` command can be used along
with the *PID* to terminate any processes that are using large amounts of resource.

> ## Login Node Etiquette
> Which of these commands would probably be okay to run on the login node?
> 
> 1. python physics_sim.py
> 2. make
> 3. create_directories.sh
> 4. molecular_dynamics_2
> 5. tar -xzf R-3.3.0.tar.gz
>
> > ## Solution
> > 1. Likely not OK - the name of the python program indicates it may run a resource intensive simulation.
> > 2. OK - the login nodes can be used for building software unless the compiles take a very long time.
> > 3. OK - A shell script used to manage data will usually be fine to run on the login nodes.
> > 4. Likely not OK - the name of the program implies that it may run a resource intensive simulation.
> > 5. OK - Expanding small data archives would usually be fine on the login nodes. Extracting very large
> >    data archives may be better suited to running on a data analysis node.
> {: .solution}
{: .challenge}

If you experience performance issues with a login node you should report it to the
[ARCHER2 Service Desk](https://www.archer2.ac.uk/support-access/servicedesk.html) for them
to investigate.

You should not use ARCHER2 login nodes to login to other, external services. Outgoing SSH
connections will be killed.

## Do not share your login credentials

You should not share your login details (account name, passwords or SSH keys) with anyone else. If 
we detect evidence of account sharing of this form we will require you to reset your access credentials.

Accessing another ARCHER2 user account from your account is also not allowed (as this would
allow you to potentially capture the credentials for the other account). If we detect this
behaviour we will require both people involved to reset their access credentials.

## Test before scaling

Remember that you are charged for usage on ARCHER2. A simple mistake in a 
job script can end up costing a large amount of your resource budget. Imagine a job script with 
a mistake that makes it sit doing nothing for 24 hours on 1000 cores or one where you have
requested 2000 cores by mistake and only use 100 of them. This problem can be compounded 
if you write scripts that automate job submission (for example, when running the same
calculation or analysis over lots of different input).  When this happens it hurts both you
(as you waste lots of charged resource) and other users (who are blocked from accessing the
idle compute nodes).

Also, if ARCHER2 is very busy you may wait in the queue for your job to fail within 10 seconds
of starting due to a trivial typo in the job script. This is extremely frustrating! You can 
use the ARCHER2 test queues to run short correctness tests on your job scripts before submitting
the full calculation.

<!-- TODO: Add in syntax for ARCHER2 test and development queues -->

> ## Test job submission scripts that use large amounts of resource
> Before submitting a large run of jobs, submit one as a test first to make sure everything works
> as expected.
>
> Before submitting a very large or very long job submit a short truncated test to ensure that
> the job starts as expected.
{: .callout}

## Have a backup plan

Although the ARCHER2 /home file systems are backed up, the /work file systems are not,
and /home is only backed up for disaster recovery purposes (*i.e.* for restoring the
whole file system if lost rather than an individual file or directory you have deleted by mistake).
Your data on ARCHER2 is primarily your responsibility and you should ensure you have secure copies of data
that are critical to your work.

Version control systems (such as Git) often have free, cloud-based offerings (e.g. Github, Gitlab)
that are generally used for storing source code. Even if you are not writing your own 
programs, these can be very useful for storing job scripts, analysis scripts and small
input files. 

For larger amounts of data, you should make sure you have a robust system in place for taking
copies of critical data off ARCHER2 wherever possible to backed-up storage. Tools such
as `rsync` can be very useful for this.

Your access to ARCHER2 will generally be time-limited so you should ensure you have a
plan for transferring your data off the system before your access finishes. The time required to
transfer large amounts of data should not be underestimated and you should ensure you have planned
for this early enough (ideally, before you even start using the system for your research).

As already mentioned, the ARCHER2 User and Best Practice Guide provides a lot of useful information
on managing and transferring your data. See:

* https://docs.archer2.ac.uk/user-guide/data.html

> ## Your data is your responsibility
> Make sure you understand what the backup policy is on ARCHER2 and what implications this has for
> your work if you lose your data on the system. Plan your backups of critical data and how you will
> transfer data off the system throughout the project. 
{: .callout}

## Transferring data

As mentioned above, many users run into the challenge of transferring large amounts of data 
off HPC systems at some point (this is more often in transferring data off-of than on-to systems,
but the advice below applies in either case). Data transfer speed may be limited by many
different factors so the best data transfer mechanism to use depends on the type of data being
transferred and where the data is going. Some of the key issues to be aware of are:

- **Disk speed** - The ARCHER2 /work file systems are highly parallel, consisting of a very
  large number of high performance disk drives. This allows them to support a very high data
  bandwidth. Unless the remote system has a similar parallel file system you may find your
  transfer speed limited by disk performance at that end.
- **Meta-data performance** - *Meta-data operations* such as opening and closing files or
  listing the owner or size of a file are much less parallel than read/write operations. If
  your data consists of a very large number of small files you may find your transfer speed is
  limited by meta-data operations. Meta-data operations performed by other users on ARCHER2
  can also interact strongly with your work so reducing the number of such operations
  you use (by combining multiple files into a single file) may reduce variability in your transfer
  rates and increase transfer speeds.
- **Network speed** - Data transfer performance can be limited by network speed. More importantly,
  it is limited by the slowest section of the network between source and destination. If you are
  transferring to your laptop/workstation, this is likely to be its connection (either via LAN or 
  wifi).
- **Firewall speed** - Most modern networks are protected by some form of firewall that filters
  out malicious traffic. This filtering has some overhead and can result in a reduction in data
  transfer performance. The needs of a general purpose network that hosts email/web-servers and
  desktop machines are quite different from a research network that needs to support high volume
  data transfers. If you are trying to transfer data to or from a host on a general purpose
  network you may find the firewall for that network will limit the transfer rate you can achieve.

As mentioned above and earlier in this lesson, if you have related data that consists of a large number of small files it
is strongly recommended to pack the files into a larger *archive* file for long term storage and
transfer. A single large file makes more efficient use of the file system and is easier to move,
copy and transfer because significantly fewer meta-data operations are required. Archive files can
be created using tools like `tar` and `zip`.

> ## Consider the best way to transfer data
> If you are transferring large amounts of data you will need to think about what may affect your transfer
> performance. It is always useful to run some tests that you can use to extrapolate how long it will
> take to transfer your data.
>
> If you have many files, it is best to combine them into an archive file before you transfer them using a
> tool such as `tar`.
{: .callout}


{% include links.md %}


