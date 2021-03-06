FROM ubuntu:16.04

ENV WORKSPACE_DIR /home/shairegular
ENV CATKIN_WS ${WORKSPACE_DIR}/catkin_ws
ENV DRONE_DEMO_DIR_DEST ${CATKIN_WS}/src/py-control-with-mavros
ENV DRONE_SCRIPT_DIR_DEST ${CATKIN_WS}/src/scripts
ENV FIRMWARE_DIR ${WORKSPACE_DIR}/Firmware

# the below will run as root until creation of a new user 
RUN apt-get update && \
    apt-get install -y git \
                       lsb-release
# install vim for easier debugging / editing
RUN apt-get install -y vim

# install killall command used by demo scripts
RUN apt-get install -y psmisc

# Add ROS to sources.list
RUN echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list && \
    apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116 && \
    apt-get update

# Install gazebo with ROS
RUN apt-get update && \
    apt-get install -y ros-kinetic-gazebo-ros-control \
                       ros-kinetic-gazebo-ros-pkgs

# Initialize rosdep (for later build with catkin)
RUN ["/bin/bash", "-c", "\
    rosdep init && \
    rosdep update \
"]

# Install catkin
RUN apt-get update && \
    apt-get install -y python-catkin-tools
RUN mkdir -p ${CATKIN_WS}/src

# Install mavros (https://dev.px4.io/en/ros/mavros_installation.html)
RUN apt-get update && \
    apt-get install -y python-wstool \
                       python-rosinstall-generator \
                       python-catkin-tools

# Checkout and build Firmware
RUN git clone https://github.com/PX4/Firmware.git ${FIRMWARE_DIR}
RUN git -C ${FIRMWARE_DIR} submodule update --init --recursive

ENV GAZEBO_MODEL_PATH ${GAZEBO_MODEL_PATH}:${MODELS_DIR}

RUN apt-get update && \
    apt-get install -y libopencv-dev \
                       protobuf-compiler \
                       python-jinja2 \
                       python-toml

ENV QT_X11_NO_MITSHM=1

# Create the user shairubin - not sure we need the workdir below 
#RUN useradd -d /home/shairegular -ms /bin/bash -g root -G sudo -p ubuntu shairegular
#USER shairegular
#WORKDIR /home/shairegular

RUN ["/bin/bash", "-c", "\
    source /opt/ros/kinetic/setup.bash && \
    mkdir -p ${CATKIN_WS}/src && \
    catkin init -w ${CATKIN_WS} && \
    wstool init ${CATKIN_WS}/src && \
    rosinstall_generator --upstream mavros | tee /tmp/mavros.rosinstall && \
    rosinstall_generator mavlink | tee -a /tmp/mavros.rosinstall && \
    wstool merge -t ${CATKIN_WS}/src /tmp/mavros.rosinstall && \
    wstool update -t ${CATKIN_WS}/src && \
    rosdep install --from-paths ${CATKIN_WS}/src --ignore-src --rosdistro kinetic -y \
"]

# prepare drone_demo code for a build
COPY py-control-with-mavros ${DRONE_DEMO_DIR_DEST} 
COPY my_scripts ${DRONE_SCRIPT_DIR_DEST}

# run catkin build for all packages 
RUN ["/bin/bash", "-c", "\
    source /opt/ros/kinetic/setup.bash && \
    catkin build -w ${CATKIN_WS} \
"]

RUN ${CATKIN_WS}/src/mavros/mavros/scripts/install_geographiclib_datasets.sh

# Install avoidance module dependencies
#RUN apt-get update && \
#    apt-get install -y libpcl1 \
#                       ros-kinetic-octomap-*

# Prepare and build avoidance
#COPY global_planner ${AVOIDANCE_DIR}
#COPY sim/models ${MODELS_DIR}
#COPY sim/worlds ${WORLDS_DIR} 

# NOTE: catkin build fails the first time (maybe the modules have to be built in the right order?)
RUN ["/bin/bash", "-c", "\
    source /opt/ros/kinetic/setup.bash && \
    catkin build -w ${CATKIN_WS}; catkin build -w ${CATKIN_WS} \
"]

# Checkout and build Firmware
#RUN git clone https://github.com/PX4/Firmware.git ${FIRMWARE_DIR}
#RUN git -C ${FIRMWARE_DIR} submodule update --init --recursive

#ENV GAZEBO_MODEL_PATH ${GAZEBO_MODEL_PATH}:${MODELS_DIR}

#RUN apt-get update && \
#    apt-get install -y libopencv-dev \
#                       protobuf-compiler \
#                       python-jinja2 \
#                       python-toml

#ENV QT_X11_NO_MITSHM=1

#RUN ["/bin/bash", "-c", " \
#    cd ${FIRMWARE_DIR} && \
#    . ${FIRMWARE_DIR}/Tools/setup_gazebo.bash ${FIRMWARE_DIR} ${FIRMWARE_DIR}/build/posix_sitl_default && \
#    DONT_RUN=1 make posix_sitl_default gazebo \
#"]
RUN ["/bin/bash", "-c", " \
    cd ${FIRMWARE_DIR} && \
    . ${FIRMWARE_DIR}/Tools/setup_gazebo.bash ${FIRMWARE_DIR} ${FIRMWARE_DIR}/build/posix_sitl_default && \
    DONT_RUN=1 make posix_sitl_default gazebo_iris \
"]

# Start avoidance simulation
#CMD ["/bin/bash", "-c", " \
#    source /opt/ros/kinetic/setup.bash && \
#    source ${CATKIN_WS}/devel/setup.bash && \
#    export ROS_PACKAGE_PATH=${ROS_PACKAGE_PATH}:${FIRMWARE_DIR} && \
#    . ${FIRMWARE_DIR}/Tools/setup_gazebo.bash ${FIRMWARE_DIR} ${FIRMWARE_DIR}/build/posix_sitl_default && \
#    roslaunch global_planner global_planner_sitl_mavros.launch world_path:=${WORLDS_DIR}/test_city_2.world \
#"]
RUN echo 'Shai Rubin Container'
CMD ["/home/shairegular/catkin_ws/src/scripts/start_px4.sh"]
