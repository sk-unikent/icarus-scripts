#!/bin/bash
#SBATCH --nodes=1
#SBATCH --partition=gpu-p100
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=ExampleTensorflowApplication
#SBATCH --mail-type=END
#SBATCH --mail-user=USERNAME@kent.ac.uk
#SBATCH --output=/home/USERNAME/slurm/logs/%j.out

python /home/USERNAME/slurm/examples/tensorflow.py
