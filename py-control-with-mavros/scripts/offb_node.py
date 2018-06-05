#!/usr/bin/env python
import rospy
import mavros
import mavros_msgs
import copy 
import pprint
#from communication import state_cb, current_state
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State 
from mavros_msgs.srv import SetMode, CommandBool, CommandTOL
from tf.transformations import quaternion_from_euler


current_state = State() 
 
def state_cb(state):    # when state changed this function will be called 
    global current_state
    rospy.logdebug("State callback function!")
    current_state = state
    rospy.logdebug(pprint.pformat(state))

rospy.loginfo('Start setting Publishers and Subscribers') 
rospy.init_node('offb_node', anonymous=True) 


def setup(commHub):     
    global current_state
    startUpPose = PoseStamped()
    startUpPose.pose.position.x = 0
    startUpPose.pose.position.y = 0
    startUpPose.pose.position.z = 2

    rospy.loginfo("Start changeOffboardModeAndArm"); 
    # send a few setpoints before starting
    rospy.loginfo('send a few setpoints before starting')
    for i in range(100):
        commHub.local_pos_pub.publish(startUpPose)
        commHub.rate.sleep()

    rospy.loginfo('wait for FCU connection')    
    # wait for FCU connection
    while not current_state.connected:
        commHub.rate.sleep()    
    rospy.loginfo('FCU connected !')    


def changeOffboardModeAndArm(commHub):
    global current_state
    startUpPose = PoseStamped()
    startUpPose.pose.position.x = 0
    startUpPose.pose.position.y = 0
    startUpPose.pose.position.z = 2

    prev_state = current_state 
    duration = rospy.Duration(5.)
    last_request = rospy.get_rostime()
    loops =0; 
    while (not rospy.is_shutdown() and current_state.armed == False): 
        loops+=1
        if (loops % 30 ==0 ):
            rospy.logdebug("Current mode: %s " % current_state.mode)
        now = rospy.get_rostime()
        if current_state.mode != "OFFBOARD" and (now - last_request > duration) :
            rospy.loginfo('setting mode to OFFBOARD')
            commHub.set_mode_client(base_mode=0, custom_mode="OFFBOARD")
            last_request = now 
        else:
            if not current_state.armed and (now - last_request > duration):
               rospy.loginfo('Arming client')
               commHub.arming_client_cmd(True)
               last_request = now 

        # older versions of PX4 always return success==True, so better to check Status instead
        if prev_state.armed != current_state.armed:
            rospy.loginfo("Vehicle armed: %r" % current_state.armed)
        if prev_state.mode != current_state.mode: 
            rospy.loginfo("Current mode changed to: %s" % current_state.mode)
        prev_state = current_state

        # Update timestamp and publish pose 
        startUpPose.header.stamp = rospy.Time.now()
        commHub.local_pos_pub.publish(startUpPose)
        commHub.rate.sleep()

    rospy.loginfo("\t Vehicle armed: %r" % current_state.armed)
    rospy.loginfo("\t Current mode: %s" % current_state.mode)
    rospy.loginfo("End changeOffboardModeAndArm with %d iterations" %loops); 




def land(commHub):
    global current_state
    rospy.loginfo("trying to land");
# landing procedure -- send land messages until successfull command 
    land_response = commHub.land_client(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
    loops = 0
    while (land_response.success == False and loops < 200):
      loops+=1 
      rospy.loginfo("sending landing command again")
      land_response = commHub.land_client(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
      print(land_response.success)
      commHub.rate.sleep()
# wait for engines to stop 
    if (loops == 200):
        rospy.logerror("Cannot land!")
    
    while (current_state.armed == True):
        commHub.rate.sleep()


def executeMission(commHub, navigation): 
    global current_state
    pose = PoseStamped()

    pose.pose.position.x = 3
    pose.pose.position.y = 3
    pose.pose.position.z =3
    pose.pose.orientation.x=0
    pose.pose.orientation.y=0
    pose.pose.orientation.z=0.7070
    pose.pose.orientation.w=0.7070

# RPY to convert: 90deg, 0, -90deg
    #q = quaternion_from_euler(0, 0, -3.14)
    #print "The quaternion representation is %s %s %s %s." % (q[0], q[1], q[2], q[3])


    rospy.loginfo("**Start executeMission"); 
    navigation.gotoPose(pose, commHub)        
    pose.pose.position.x = -2
    pose.pose.position.y = -2
    pose.pose.position.z = 1
    pose.pose.orientation.x=0
    pose.pose.orientation.y=0
    pose.pose.orientation.z=0
    pose.pose.orientation.w=1
    navigation.gotoPose(pose, commHub)
    pose.pose.position.x = -2
    pose.pose.position.y = 3
    pose.pose.position.z = 2
    pose.pose.orientation.x=0
    pose.pose.orientation.y=0
    pose.pose.orientation.z=-0.7070
    pose.pose.orientation.w=0.7070
    navigation.gotoPose(pose, commHub)
    pose.pose.position.x = 0
    pose.pose.position.y = 0
    pose.pose.position.z = 1
    pose.pose.orientation.x=0
    pose.pose.orientation.y=0
    pose.pose.orientation.z=-1
    pose.pose.orientation.w=0
    navigation.gotoPose(pose, commHub)
    land(commHub)
    rospy.loginfo("\t Vehicle armed: %r" % current_state.armed)
    rospy.loginfo("\t Current mode: %s" % current_state.mode)
    rospy.loginfo("landed !")

    rospy.loginfo("**End executeMission")


def main():
    print("Start main")
    try:
        commHub = CommunicationHub() 
        setup(commHub)
        changeOffboardModeAndArm(commHub)
        navigation = Navigation()
        executeMission(commHub, navigation)
    except rospy.ROSInterruptException:
        pass

class CommunicationHub:


    def __init__(self):
        rospy.loginfo("CommunicationHub __init__")
        self.set_mode_client    = rospy.ServiceProxy('mavros/set_mode', SetMode) 
        self.arming_client_cmd  = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
        self.local_pos_pub      = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
        self.land_client        = rospy.ServiceProxy("mavros/cmd/land", CommandTOL)
        self.state_sub          = rospy.Subscriber('mavros/state', State, state_cb) # used in setup of drneCtrl 
        self.rate = rospy.Rate(20.0);  

class Navigation:
    def __init__(self):
        rospy.loginfo("Navigation __init__")  

    def gotoPose(self, pose, commHub):
        rospy.loginfo("**Start gotoPose to pose "); 
        loops =0    
        while (not rospy.is_shutdown() and loops< 200):
            loops +=1;  
            # Update timestamp and publish pose 
            pose.header.stamp = rospy.Time.now()
            commHub.local_pos_pub.publish(pose)
            commHub.rate.sleep()
        rospy.loginfo("**End gotoPose"); 
        
        
if __name__ == '__main__':
    main()

