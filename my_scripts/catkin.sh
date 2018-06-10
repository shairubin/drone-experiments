echo "removing old ROS log files"
echo "before deleting files:"
ls -1 ~/.ros/log/ | wc -l
rm -rf ~/.ros/log/*
echo "after deleting files:"
ls -1 ~/.ros/log/ | wc -l
CATDIR=$HOME/catkin_ws/
echo "CATDIR: $CATDIR" 
cd "$CATDIR"
echo "source devl/setup.bash"
source devel/setup.bash

