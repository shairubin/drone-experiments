#!/bin/bash
source $HOME/catkin_ws/src/my_scripts/catkin.sh 
source $HOME/catkin_ws/src/my_scripts/gazebo.sh

if [ "$1" = "" ]; then
        echo "ERROR - TEST SCRIPT MUST GET THE NAME OF THE MODEL TO TEST"
        exit 1 
fi
echo ""
echo Start test $1
echo ""

sleep 2
echo "start ros nodes"
$HOME/catkin_ws/src/my_scripts/start_ros_nodes.sh &
sleep 4 

echo "start px4 simulator"
$HOME/catkin_ws/src/my_scripts/start_px4.sh $1 &
sleep 4

echo "start gazebo simulator"
sleep 2
$HOME/catkin_ws/src/my_scripts/start_gazebo_ros.sh true  $1 &
sleep 5



# start of 	test section 
rosrun py-control-with-mavros offb_node.py
# end of 	test section

sleep 2
echo "kill ROS nodes"
$HOME/catkin_ws/src/my_scripts/kill_ros_nodes.sh

sleep 1 
echo "kill px4 and gazebo simulator"
$HOME/catkin_ws/src/my_scripts/kill_gazebo.sh 
