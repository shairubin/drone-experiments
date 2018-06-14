#!/bin/sh
echo "setup gazebo script"
cd ~/src/Firmware
pwd 
no_sim=1 make posix_sitl_lpe gazebo 
