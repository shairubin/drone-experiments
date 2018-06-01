#!/usr/bin/env python

import rospy
import mavros
import mavros_msgs
import copy 
import boardSetup
from DroneCtrl import DroneCtrl
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State 
from mavros_msgs.srv import SetMode, CommandBool, CommandTOL
from tf.transformations import quaternion_from_euler
#state

rospy.loginfo('Start setting Publishers and Subscribers')


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


# def setup():     
#     rospy.loginfo("Start changeOffboardModeAndArm"); 
#     # send a few setpoints before starting
#     rospy.loginfo('send a few setpoints before starting')
#     for i in range(100):
#         boardSetup.local_pos_pub.publish(pose)
#         rate.sleep()

#     rospy.loginfo('wait for FCU connection')    
#     # wait for FCU connection
#     while not boardSetup.current_state.connected:
#         rate.sleep()
    
#     rospy.loginfo('FCU connected !')    


def changeOffboardModeAndArm():
    prev_state = boardSetup.current_state 
    duration = rospy.Duration(5.)
    last_request = rospy.get_rostime()
    loops =0; 
    while (not rospy.is_shutdown() and boardSetup.current_state.armed == False): 
        loops+=1
        if (loops % 30 ==0 ):
            rospy.loginfo("Current mode: %s " %boardSetup.current_state.mode)
        now = rospy.get_rostime()
        if boardSetup.current_state.mode != "OFFBOARD" and (now - last_request > duration) :
            rospy.loginfo('setting mode to OFFBOARD')
            boardSetup.setOffBaord()
            #boardSetup.set_mode_client(base_mode=0, custom_mode="OFFBOARD")
            rospy.loginfo("Current mode after setting: %s " %boardSetup.current_state.mode)
            last_request = now 
        else:
            if not boardSetup.current_state.armed and (now - last_request > duration):
               rospy.loginfo('Arming client')
               boardSetup.arming_client_cmd(True)
               last_request = now 

        # older versions of PX4 always return success==True, so better to check Status instead
        if prev_state.armed != boardSetup.current_state.armed:
            rospy.loginfo("Vehicle armed: %r" % boardSetup.current_state.armed)
        #rospy.loginfo("Board state: %s " %boardSetup.current_state.mode)
        #rospy.loginfo("prev state: %s " %prev_state.mode)
        if prev_state.mode != boardSetup.current_state.mode: 
            rospy.loginfo("Current mode changed to: %s" % boardSetup.current_state.mode)
        prev_state = boardSetup.current_state

        # Update timestamp and publish pose 
        pose.header.stamp = rospy.Time.now()
        boardSetup.local_pos_pub.publish(pose)
        rate.sleep()

    rospy.loginfo("\t Vehicle armed: %r" % boardSetup.current_state.armed)
    rospy.loginfo("\t Current mode: %s" % boardSetup.current_state.mode)
    rospy.loginfo("End changeOffboardModeAndArm with %d iterations" %loops); 

def gotoPose(pose):
    rospy.loginfo("**Start gotoPose to pose "); 
    loops =0    
    while (not rospy.is_shutdown() and loops< 200):
        loops +=1;  
        # Update timestamp and publish pose 
        pose.header.stamp = rospy.Time.now()
        boardSetup.local_pos_pub.publish(pose)
        rate.sleep()
    rospy.loginfo("**End gotoPose"); 
def land():
    rospy.loginfo("trying to land");
# landing procedure -- send land messages until successfull command 
    land_response = boardSetup.land_client(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
    loops = 0
    while (land_response.success == False and loops < 200):
      loops+=1 
      rospy.loginfo("sending landing command again")
      land_response = boardSetup.land_client(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
      print(land_response.success)
      rate.sleep()
# wait for engines to stop 
    if (loops == 200):
        rospy.logerror("Cannot land!")
    
    while (boardSetup.current_state.armed == True):
        rate.sleep()


def executeMission(): 
    pose.pose.position.x = 3
    pose.pose.position.y = 3
    pose.pose.position.z =3
    pose.pose.orientation.x=0
    pose.pose.orientation.y=0
    pose.pose.orientation.z=0.7070
    pose.pose.orientation.w=0.7070

# RPY to convert: 90deg, 0, -90deg
    q = quaternion_from_euler(0, 0, -3.14)
    print "The quaternion representation is %s %s %s %s." % (q[0], q[1], q[2], q[3])


    rospy.loginfo("**Start executeMission"); 
    #gotoPose(pose)        
    pose.pose.position.x = -2
    pose.pose.position.y = -2
    pose.pose.position.z = 1
    pose.pose.orientation.x=0
    pose.pose.orientation.y=0
    pose.pose.orientation.z=0
    pose.pose.orientation.w=1
    #gotoPose(pose)
    pose.pose.position.x = -2
    pose.pose.position.y = 3
    pose.pose.position.z = 2
    pose.pose.orientation.x=0
    pose.pose.orientation.y=0
    pose.pose.orientation.z=-0.7070
    pose.pose.orientation.w=0.7070
    #gotoPose(pose)
    pose.pose.position.x = 0
    pose.pose.position.y = 0
    pose.pose.position.z = 1
    pose.pose.orientation.x=0
    pose.pose.orientation.y=0
    pose.pose.orientation.z=-1
    pose.pose.orientation.w=0
    gotoPose(pose)
    land()
    rospy.loginfo("\t Vehicle armed: %r" % boardSetup.current_state.armed)
    rospy.loginfo("\t Current mode: %s" % boardSetup.current_state.mode)
    rospy.loginfo("landed !")

    rospy.loginfo("**End executeMission")


def main():
    print("Start main")
    try:
        ctrl = DroneCtrl() 
        ctrl.setup(rate)
        #ctrl.changeOffboardModeAndArm(rate, boardSetup.set_mode_client)
        changeOffboardModeAndArm()
        executeMission()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()

