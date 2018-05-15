#!/bin/bash
echo "kill gazebo and px4"
cd /home/shairegular/catkin_ws/
source ./devel/setup.bash
killall -9 start_gazebo.sh
sleep 1s
killall -9 gzclient
sleep 1s
killall -9 gzserver
sleep 1s 
killall -9 px4


