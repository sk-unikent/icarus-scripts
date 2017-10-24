#!/bin/bash

# Install Anaconda.
/bin/bash /opt/icarus/Anaconda3-5.0.0.1-Linux-x86_64.sh -b -p $HOME/anaconda

# Setup environment (overwrites .bash* files).
cp /opt/icarus/env/* ~/

# Do this here now, rather than sourcing all of that.
PATH=$HOME/.local/bin:$HOME/anaconda/bin:$HOME/bin:$PATH
export PATH

# Update conda.
conda update --all -y

# Create log directory for Slurm.
mkdir -p ~/slurm/logs
