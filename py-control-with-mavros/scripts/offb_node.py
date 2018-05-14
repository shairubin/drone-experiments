#!/usr/bin/env python

import rospy
import mavros
import mavros_msgs
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State 
from mavros_msgs.srv import SetMode, CommandBool

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
set_mode_client = rospy.ServiceProxy('mavros/set_mode', SetMode) 

pose = PoseStamped()
pose.pose.position.x = 0
pose.pose.position.y = 0
pose.pose.position.z = 2

def changeOffboardModeAndArm():
     
    rospy.init_node('offb_node', anonymous=True)
    rospy.loginfo("Start changeOffboardModeAndArm"); 
    rospy.loginfo("End changeOffboardModeAndArm"); 

def position_control():
    rospy.loginfo('Start of position_control function')

    prev_state = current_state
    rate = rospy.Rate(20.0) # MUST be more then 2Hz

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

    last_request = rospy.get_rostime()
    while (not rospy.is_shutdown() and (not current_state.armed)):
#        rospy.loginfo('inside loop')
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

    rospy.loginfo("End of position_control")
    rospy.loginfo("Vehicle armed: %r" % current_state.armed)
    rospy.loginfo("Current mode: %s" % current_state.mode)


def main():
    print("Hello world")
    try:
        rospy.loginfo('Start __main__')
        changeOffboardModeAndArm()
        position_control()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()
