Tensorflow on Icarus
===

We have a special tensorflow build for icarus-gpu-01 which takes full advantage of the hardware.
This guide assumes you have already setup your environment as detailed in "Python on Icarus".

Tensorflow should be installed via our setup script (/opt/icarus/setup.py), we currently have version 1.5.0 available. If you require a different version please let us know.

After installation, run the example:
```
sbatch ~/slurm/examples/tensorflow.sh
```

Check the slurm logs for output.
