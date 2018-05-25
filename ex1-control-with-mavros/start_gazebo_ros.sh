#!/bin/sh
echo "setup gazebo script"
cd ~/src/Firmware
pwd 
roslaunch gazebo_ros empty_world.launch world_name:=/home/shairegular/src/Firmware/Tools/sitl_gazebo/worlds/iris_fpv_cam.world
