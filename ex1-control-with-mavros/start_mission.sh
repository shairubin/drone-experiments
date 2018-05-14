#!/bin/bash
echo "start mission script"
cd /home/shairegular/catkin_ws/
source ./devel/setup.bash 
rosrun ex1-control-with-mavros mission
