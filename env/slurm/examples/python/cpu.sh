#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=ExampleApplication
#SBATCH --mail-type=END
#SBATCH --mail-user=USERNAME@kent.ac.uk
#SBATCH --output=/home/USERNAME/slurm/logs/%j.out

python /home/USERNAME/slurm/examples/python/example.py
