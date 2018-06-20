#!/bin/sh
echo "setup gazebo script"
cd ~/src/Firmware
simenv=$1
echo $simenv
pwd 
if [ "$simenv" = "lpe" ]; then 
	echo "start px4 in lpe mode with with optical flow simulation"
	sleep 3
	no_sim=1 make posix_sitl_lpe gazebo_iris_opt_flow  
elif [ "$simenv" = "default" ]; then 
	echo "start px4 in efk2 mode and gps-based simulation"
	sleep 3
	no_sim=1 make posix_sitl_default gazebo_iris
elif [ "$simenv" = "rplidar" ]; then 
	echo "start px4 in lpe mode and rplidar simulation"
	sleep 3
	no_sim=1 make posix_sitl_lpe gazebo_iris_rplidar

else 
	echo "unsupported mode"

fi 	
