#!/bin/sh
echo "start roscore nodee "
cd /home/shairegular/catkin_ws/
roscore &
sleep 2s
echo "start mavros node "
cd /home/shairegular/catkin_ws/
roslaunch mavros px4.launch fcu_url:="udp://:14540@127.0.0.1:14540" &
