#!/bin/bash

# Install Anaconda.
/bin/bash /opt/icarus/Anaconda3-5.0.0.1-Linux-x86_64.sh -b -p $HOME/anaconda

# Setup bash environment.
cp /opt/icarus/env/.bash* ~/
