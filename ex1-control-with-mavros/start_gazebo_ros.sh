#!/bin/sh
echo "start gazebo throu roslaunch"
cd ~/src/Firmware
pwd 
#roslaunch gazebo_ros empty_world.launch world_name:=/home/shairegular/src/Firmware/Tools/sitl_gazebo/worlds/iris_opt_flow.world gui:=$1 
roslaunch gazebo_ros $2_world.launch world_name:=/home/shairegular/catkin_ws/src/gazebo/worlds/iris_fpv_my_cam.world gui:=$1
