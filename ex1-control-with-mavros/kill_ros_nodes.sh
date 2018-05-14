#!/bin/bash
echo "kill mavros node "
cd /home/shairegular/catkin_ws/
source ./devel/setup.bash
# kill command heresource devel/setup.bash
rosnode kill mavros
sleep 2s
echo "kill roscore and rosmaster nodes"
killall -9 roscore
killall -9 rosmaster

