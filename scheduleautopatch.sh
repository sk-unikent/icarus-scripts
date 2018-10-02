#!/bin/bash

rm /tmp/_autopatch.sh
sinfo -N | awk '{print "srun --nodelist="$1" --partition="$3" /opt/slurm/autopatch.sh &"}' | tail -n +2 | sed 's/*//g' > /tmp/_autopatch.sh
chmod 0700 /tmp/_autopatch.sh
/tmp/_autopatch.sh
