#!/bin/bash
source $HOME/catkin_ws/src/my_scripts/catkin.sh 
source $HOME/catkin_ws/src/my_scripts/gazebo.sh

echo "start test1 node "
sleep 2
echo "start ros nodes"
$HOME/catkin_ws/src/ex1-control-with-mavros/start_ros_nodes.sh &
sleep 4 

echo "start px4 simulator"
$HOME/catkin_ws/src/ex1-control-with-mavros/start_px4.sh default &
sleep 4

echo "start gazebo simulator"
sleep 2
$HOME/catkin_ws/src/ex1-control-with-mavros/start_gazebo_ros.sh true  default &
sleep 6



# start of 	test section 
rosrun py-control-with-mavros offb_node.py
# end of 	test section

sleep 5
echo "kill ROS nodes"
$HOME/catkin_ws/src/ex1-control-with-mavros/kill_ros_nodes.sh

sleep 1 
echo "kill px4 and gazebo simulator"
$HOME/catkin_ws/src/ex1-control-with-mavros/kill_gazebo.sh 
