---
title: "Post-simulation analysis"
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

For this course, we have prepared a number of exercises. You can get a copy of 
these exercises by running (make sure to run this from `/work`):

```bash
svn checkout https://github.com/EPCCed/archer2-advanced-use-of-lammps/trunk/exercises
```

Once this is downloaded, please  `cd exercises/1-performance-exercise/`. In this 
directory you will find three files:
{% include links.md %}
