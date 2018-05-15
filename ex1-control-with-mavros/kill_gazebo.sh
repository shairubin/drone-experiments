#!/bin/bash
echo "kill gazebo and px4"
cd /home/shairegular/catkin_ws/
source ./devel/setup.bash
killall -9 gazebo
sleep 1s
killall -9 px4
sleep 1s 
killall -9 gzserver


