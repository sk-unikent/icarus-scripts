#!/bin/bash
# Puppet managed script

/usr/bin/yum -q -y update
sleep 1
/sbin/grubby --default-kernel >/var/spool/nagios/next_kernel.txt
sleep 1
/opt/nrpe/check_kernel.sh || /sbin/reboot
