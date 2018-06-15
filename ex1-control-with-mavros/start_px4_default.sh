#!/bin/sh
echo "setup gazebo script"
cd ~/src/Firmware
pwd 
# the first argument for make is the *config* target (i.e., how the board of px4 should be configured ) 
# and the second argument is the *make* target (i.e., what is the type of the board - hardware/firmware)
# see description in https://dev.px4.io/en/setup/building_px4.html 
# the full desxription of the build command is described here https://dev.px4.io/en/simulation/
# two usefull commands
# 		* make posix list_vmd_make_targets
# 		* make list_config_targets 
#no_sim=1 make posix_sitl_efk2 gazebo_iris_opt_flow 
no_sim=1 make posix_sitl_default gazebo_iris 
