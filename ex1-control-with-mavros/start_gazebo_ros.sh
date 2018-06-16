#!/bin/sh
echo "start gazebo throu roslaunch"
cd ~/src/Firmware
pwd 
simenv=$2 
if [ "$simenv" = "lpe" ]; then 
	echo "start gazebo with optical flow iris"
	sleep 3  
	roslaunch gazebo_ros empty_world.launch world_name:=/home/shairegular/src/Firmware/Tools/sitl_gazebo/worlds/iris_opt_flow.world gui:=$1 
elif [ "$simenv" = "default" ]; then 
	echo "start gazebo in default mode with iris+camera"
	sleep 3
	roslaunch gazebo_ros empty_world.launch world_name:=/home/shairegular/catkin_ws/src/gazebo/worlds/iris_fpv_my_cam.world gui:=$1
else 
	echo "unsupported gazebo mode"

fi 	

