Python on Icarus
===

This guide will tell you how to setup your environment for running Python on Icarus.

All of these commands should be run on `icarus`, and assumes you are starting in your home directory having not done anything else since logging into the server for the first time.
If that's not the case, you'll have to make any adjustments according to any changes you may have made.

The first thing we will do is install Anaconda, which is a distribution of Python with some handy extras.
For the purposes of this guide, we're going to keep everything on the versions used while writing the guide and then we'll upgrade later.
Run `/bin/bash /opt/icarus/setup.sh`.
> Note: this will overwrite your .bashrc and .bash_profile scripts, if you have modified these you will want to read through the script and run commands manually.

Assume the above ran without errors, you should now log out of Icarus and log back in.
You can, instead, type `source .bash_profile` if you'd rather not re-login.

Type `which python`. It should return `~/anaconda/bin/python`.
