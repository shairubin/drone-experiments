#!/bin/sh
echo "start test1 node "
cd /home/shairegular/catkin_ws/
echo "start ros nodes"
/home/shairegular/catkin_ws/src/ex1-control-with-mavros/start_ros_nodes.sh &
sleep 4 
echo "start gazebo simulator"
/home/shairegular/catkin_ws/src/my_scripts/gazebo.sh
sleep 2
/home/shairegular/catkin_ws/src/ex1-control-with-mavros/start_gazebo_ros.sh true  default &
sleep 6

echo "start px4 simulator"
/home/shairegular/catkin_ws/src/ex1-control-with-mavros/start_px4.sh default &
sleep 6


# start test section 
rosrun py-control-with-mavros offb_node.py
# end of test section

sleep 5
echo "kill ros nodes"
/home/shairegular/catkin_ws/src/ex1-control-with-mavros/kill_ros_nodes.sh

sleep 5 
echo "kill px4 and simulator"
/home/shairegular/catkin_ws/src/ex1-control-with-mavros/kill_gazebo.sh 
