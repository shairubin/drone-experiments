
## PRE-REQ
1. ROS isntalled (lunar)
2. GAZEBO installed with ROS
3. PX4 installed
 
## DEMO and Test 
1. ~/catkin_ws/src/my_scripts/test1.sh
Essentially, this test script is all you need to understand the development environment below 
## Setup development environment:
1. open 4 uxterms: uxterm1, uxterm2, uxterm3, uxterm4  
2. In each run 'source catkin_ws/src/my_scripts/catkin.sh'
3. In uxterm4 also run  'source src/my_scripts/gazebo.sh'
4. In uxterm2 run './src/ex1-control-with-mavros/start_ros_nodes.sh'
5. In uxterm3 run './src/ex1-control-with-mavros/start_px4.sh'
6. in uxterm4 run './src/ex1-control-with-mavros/start_gazebo_ros.sh <bool>' bool is either 'true' or 'false' to indicate gazebo with/without ui

## Sample run 
1. In uxterm1 run *rosrun py-control-with-mavros offb_node.py*

## Set up ROS environment (lunar)
1. source /opt/ros/lunar/setup.sh
2. catkin_make  
3. source devel/setup.bash
4. echo $ROS_PACKAGE_PATH - shuld get you soemthing like ..catkin_ws/src:/opt/ros/lunar/share 
5. rospack find roscpp -- should see roscpp in the share directory
6. cd src/
7. rm py-control-with-mavros/CMakeLists.txt 
8. rm py-control-with-mavros/package.xml 
9. rm -rf py-control-with-mavros/src
10. catkin_create_pkg py-control-with-mavros rospy mavros std_msgs mavros_msgs diagnostic_msgs
11. . ~/catkin_ws/devel/setup.bash
12. rospack depends1 py-control-with-mavros -- verify you get all the packages above
13. now you should be able to run the rosrun command above

## Collecting Diagnostics and messages   
1. Set up development environment as above 
2. Open one more uxterm 
3. In this uxterm do *source ~/catkin_ws/src/my_scripts/catkin.sh* 
4. start collecting data from /Diagnostics topic. In a seperate directory do: 'rosbag record -O <bag filename> /diagnostics'
5. Do the  Sample/DEMO run as above 
6. Once Sample run finished - stop collecting (CTRL-C)
7. Extract Diagnostics data into CSV files: 'rosrun diagnostic_analysis export_csv.py <bag filename>.bag -d .'. You will get an 'output' file
8. On another note *'rostopic echo \<topic name\>'* will print messages

## using rosbag 
1.  playing a subset of the topics: *'rosbag play \<bag_file name\> --topic \<topic name\>*   

## Using Docker
1. How to log-in into a **running container**: *'docker exec -it \<container name\> /bin/bash'*
2. How to start a container from an image with interactive shell: sudo docker run -t -i \<image id\> /bin/bash 
