FIRMPLACE=$HOME/src/Firmware
echo "FRIMPLACE: $FIRMPLACE"
cd "$FIRMPLACE"
source Tools/setup_gazebo.bash $(pwd) $(pwd)/build/posix_sitl_default
cd "$CATDIR"

