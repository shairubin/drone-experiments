#!/usr/bin/env python

import rospy
import mavros
import mavros_msgs
import copy 
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State 
from mavros_msgs.srv import SetMode, CommandBool, CommandTOL

# callback method for state sub
current_state = State() 
offb_set_mode = SetMode
def state_cb(state):
    global current_state
    current_state = state

#local_pos_pub = rospy.Publisher(mavros.get_topic('setpoint_position', 'local'), PoseStamped, queue_size=10)
rospy.loginfo('Start setting Publishers and Subscribers')
 
local_pos_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
state_sub = rospy.Subscriber('mavros/state', State, state_cb)
arming_client = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
land_client = rospy.ServiceProxy("mavros/cmd/land", CommandTOL)
set_mode_client = rospy.ServiceProxy('mavros/set_mode', SetMode) 
rospy.init_node('offb_node', anonymous=True) 
rate = rospy.Rate(20.0);  
pose = PoseStamped()
pose.pose.position.x = 0
pose.pose.position.y = 0
pose.pose.position.z = 2

land_cmd = CommandTOL()
land_cmd.yaw = 0;
land_cmd.atitude = 0;
land_cmd.longitude = 0;
land_cmd.altitude = 0;


def setup():     
    rospy.loginfo("Start changeOffboardModeAndArm"); 
    # send a few setpoints before starting
    rospy.loginfo('send a few setpoints before starting')
    for i in range(100):
        local_pos_pub.publish(pose)
        rate.sleep()

    rospy.loginfo('wait for FCU connection')    
    # wait for FCU connection
    while not current_state.connected:
        rate.sleep()
    
    rospy.loginfo('FCU connected !')    


def changeOffboardModeAndArm():
    prev_state = current_state 
    last_request = rospy.get_rostime()
    loops =0; 
    while (not rospy.is_shutdown() and current_state.armed == False): 
        loops+=1
        now = rospy.get_rostime()
        if current_state.mode != "OFFBOARD" and (now - last_request > rospy.Duration(5.)):
            rospy.loginfo('setting mode to OFFBOARD')
            set_mode_client(base_mode=0, custom_mode="OFFBOARD")
            last_request = now 
        else:
            if not current_state.armed and (now - last_request > rospy.Duration(5.)):
               rospy.loginfo('Arming client')
               arming_client(True)
               last_request = now 

        # older versions of PX4 always return success==True, so better to check Status instead
        if prev_state.armed != current_state.armed:
            rospy.loginfo("Vehicle armed: %r" % current_state.armed)
        if prev_state.mode != current_state.mode: 
            rospy.loginfo("Current mode: %s" % current_state.mode)
        prev_state = current_state

        # Update timestamp and publish pose 
        pose.header.stamp = rospy.Time.now()
        local_pos_pub.publish(pose)
        rate.sleep()

    rospy.loginfo("\t Vehicle armed: %r" % current_state.armed)
    rospy.loginfo("\t Current mode: %s" % current_state.mode)
    rospy.loginfo("End changeOffboardModeAndArm with %d iterations" %loops); 

def gotoPose(pose):
    rospy.loginfo("**Start gotoPose"); 
    loops =0    
    while (not rospy.is_shutdown() and loops< 200):
        loops +=1;  
        # Update timestamp and publish pose 
        pose.header.stamp = rospy.Time.now()
        local_pos_pub.publish(pose)
        rate.sleep()
    rospy.loginfo("**End gotoPose"); 

def executeMission(): 
    pose.pose.position.x = 3
    pose.pose.position.y = 3
    pose.pose.position.z = 3
    rospy.loginfo("**Start executeMission"); 
    gotoPose(pose)        
    pose.pose.position.x = -2
    pose.pose.position.y = -2
    pose.pose.position.z = 1
    #gotoPose(pose)
    loops =0
    rospy.loginfo("tryng to land");
    land_response = land_client(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
    while (land_response.success == False):
      rospy.loginfo("tring to land");
      land_response = land_client(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
      print(land_response.success)
      loops += 1
      rate.sleep();

    rospy.loginfo("landed !")
    

    rospy.loginfo("**End executeMission"); 


def main():
    print("Start main")
    try:
        setup()
        changeOffboardModeAndArm()
        executeMission()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()

