#!/bin/sh
echo "kill all"
/home/shairegular/catkin_ws/src/ex1-control-with-mavros/kill_gazebo.sh
sleep 2s
/home/shairegular/catkin_ws/src/ex1-control-with-mavros/kill_ros_nodes.sh
sleep 2s
echo "start all"
/home/shairegular/catkin_ws/src/ex1-control-with-mavros/start_ros_nodes.sh 
sleep 2s
/home/shairegular/catkin_ws/src/ex1-control-with-mavros/start_gazebo.sh 
sleep 2s

