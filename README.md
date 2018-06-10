#This README would normally document whatever steps are necessary to get the application up and running.


## Setup development environment:
1. open 4 uxterms: uxterm1, uxterm2, uxterm3, uxterm4  
2. In each run 'source catkin_ws/src/my_scripts/catkin.sh'
3. In uxterm4 also run  'source src/my_scripts/gazebo.sh'
4. In uxterm2 run './src/ex1-control-with-mavros/start_ros_nodes.sh'
5. In uxterm3 run './src/ex1-control-with-mavros/start_px4.sh'
6. in uxterm4 run './src/ex1-control-with-mavros/start_gazebo_ros.sh <bool>' bool is either 'true' or 'false' to indicate gazebo with/without ui

## Sample run 
1. In uxterm1 run 'rosrun py-control-with-mavros offb_node.py' 
