Introduction to Icarus
===

Icarus is our new cluster, with 4 compute nodes and 1 gpu node.
The GPU node consists of two P100s with 32 CPU cores and ~192GIB RAM.
The compute nodes are smaller with 4GiB and 2 cores each for a total of 8 cores and 16GiB RAM.

Whilst the compute nodes are small, if there is significant usage of them we are in a position to add significant additional resource so I'd encourage its use where your application is not using the GPU.

The first thing to bear in mind when working on Icarus is that your home directory is shared between all nodes but each cluster partition will have a different global environment.
This means that whilst a script might work on icarus, or even nodes in the icarus-cpu partition, it may not work on the gpu partition.
To get around this you should try to do as much as possible in your home directory. 

Icarus uses Slurm to schedule resources. You will need to take a few additional steps to make the full use of this cluster however we have provided templates to make this as non-invasive as possible.
To run an application on the cluster you need to do one of two things.
 * If you want to run in realtime (bear in mind you may need to wait for resource to become available) you can use `srun` in front of your standard command e.g. `srun python test.py`. This should only really be used to test your environment etc.
 * If you want to "fire and forget", you can use sbatch to submit a job for processing. This is the better method as it is easier to setup.

There is a good stackoverflow comparison between `srun` and `sbatch` here: https://stackoverflow.com/questions/43767866/slurm-srun-vs-sbatch-and-their-parameters

To use `sbatch` you need to wrap your command in a shell script, see the examples below.
When you have your shell script ready you can submit via `sbatch shellscript.sh`, substituting in the script name.

CPU Application Template
===
```
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=ExampleApplication
#SBATCH --mail-type=END
#SBATCH --mail-user=example@kent.ac.uk
#SBATCH --output=/home/USERNAME/slurm/logs/%j.out
python sample.py
```

GPU Application Template
===
```
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --partition=gpu-p100
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=ExampleGPUApplication
#SBATCH --mail-type=END
#SBATCH --mail-user=example@kent.ac.uk
#SBATCH --output=/home/USERNAME/slurm/logs/%j.out
python sample.py
```