Tensorflow on Icarus
===

We have a special tensorflow build for icarus-gpu-01 which takes full advantage of the hardware.
This guide assumes you have already setup your environment as detailed in "Python on Icarus".

Tensorflow should be installed via our WHL, we currently have version 1.3.1 available. If you require a different version please let us know.
```
pip install --upgrade /opt/icarus/pkg/tensorflow-1.3.1-cp36-cp36m-linux_x86_64.whl 
```

Run the example:
```
sbatch ~/slurm/examples/tensorflow.sh
```

Check the slurm logs for output.