Python on Icarus
===

This guide will tell you how to setup your environment for running Python on Icarus.

All of these commands should be run on `icarus`, and assumes you are starting in your home directory having not done anything else since logging into the server for the first time.
If that's not the case, you'll have to make any adjustments according to any changes you may have made.

The first thing we will do is install Anaconda, which is a distribution of Python with some handy extras.
For the purposes of this guide, we're going to keep everything on the versions used while writing the guide and then we'll upgrade later.
Run `python /opt/icarus/setup.py`.
> Note: this will overwrite your .bashrc and .bash_profile scripts, if you have modified these you will want to read through the script and run commands manually.

Assume the above ran without errors, you should now log out of Icarus and log back in.
You can, instead, type `source .bash_profile` if you'd rather not re-login.

Type `which python`. It should return `~/anaconda/bin/python`.

We just copied a few examples into your home directory, it's nice to start there, even if you already know Python as it gives a bit of an introduction to Slurm.
Run the example application: `sbatch ~/slurm/examples/cpu.sh`.
You should (might take some time to be scheduled) have a new log file in `~/slurm/logs/`, cat it to see the result of the application.
You will also get an email when the job has finished.

Installing new Python packages
===
You have `conda` and `pip` at your disposal, both in your own anaconda environment.
If, say, you want to install Scipy just type `conda install scipy` or `pip install scipy`.
If you wish to install Tensorflow, please see our special-case docs.
