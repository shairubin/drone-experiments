#!/usr/bin/env python
import rospy
import mavros
import mavros_msgs
import copy 
import pprint
from drone_control import Navigation
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State 
from mavros_msgs.srv import SetMode, CommandBool, CommandTOL
from diagnostic_msgs.msg import DiagnosticStatus, DiagnosticArray

#current_state = State() 
#current_pose = PoseStamped() 
current_diagnostic = DiagnosticArray() 

def state_cb(state):    # when state changed this function will be called 
    global current_state
    rospy.loginfo("State callback function!")
    current_state = state
    rospy.logdebug(pprint.pformat(state))

def pose_cb(pose):    # when state changed this function will be called 
    global current_pose
    rospy.logdebug(rospy.get_caller_id() + "I heard pose %s", pose)
    current_pose = pose

def diag_cb(diagnosticArray_status):    
    global current_diagnostic
    rospy.loginfo(pprint.pformat(diagnosticArray_status))
    current_diagnostic = diagnosticArray_status

rospy.loginfo('Start setting Publishers and Subscribers') 
rospy.init_node('offb_node', anonymous=True) 


def setup(commHub):     
    #global current_state
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
    while not commHub.getCurrentState().connected:
        commHub.rate.sleep()    
    rospy.loginfo('FCU connected !')    


def changeOffboardModeAndArm(commHub):
    #global current_state
    startUpPose = PoseStamped()
    startUpPose.pose.position.x = 0
    startUpPose.pose.position.y = 0
    startUpPose.pose.position.z = 2

    prev_state = commHub.getCurrentState()
    duration = rospy.Duration(5.)
    last_request = rospy.get_rostime()
    loops =0; 
    while (not rospy.is_shutdown() and commHub.getCurrentState().armed == False): 
        loops+=1
        if (loops % 30 ==0 ):
            rospy.logdebug("Current mode: %s " % commHub.getCurrentState().mode)
        now = rospy.get_rostime()
        if commHub.getCurrentState().mode != "OFFBOARD" and (now - last_request > duration) :
            rospy.loginfo('setting mode to OFFBOARD')
            commHub.set_mode_client(base_mode=0, custom_mode="OFFBOARD")
            last_request = now 
        else:
            if not commHub.getCurrentState().armed and (now - last_request > duration):
               rospy.loginfo('Arming client')
               commHub.arming_client_cmd(True)
               last_request = now 

        # older versions of PX4 always return success==True, so better to check Status instead
        if prev_state.armed != commHub.getCurrentState().armed:
            rospy.loginfo("Vehicle armed: %r" % commHub.getCurrentState().armed)
        if prev_state.mode != commHub.getCurrentState().mode: 
            rospy.loginfo("Current mode changed to: %s" % commHub.getCurrentState().mode)
        prev_state = commHub.getCurrentState()

        # Update timestamp and publish pose 
        startUpPose.header.stamp = rospy.Time.now()
        commHub.local_pos_pub.publish(startUpPose)
        commHub.rate.sleep()

    rospy.loginfo("\t Vehicle armed: %r" % commHub.getCurrentState().armed)
    rospy.loginfo("\t Current mode: %s" % commHub.getCurrentState().mode)
    rospy.loginfo("End changeOffboardModeAndArm with %d iterations" %loops); 




# def land(commHub):


def executeMission(commHub, navigation): 
    
    pose = PoseStamped()

    pose.pose.position.x = 3
    pose.pose.position.y = 3
    pose.pose.position.z =3
    pose.pose.orientation.x=0
    pose.pose.orientation.y=0
    pose.pose.orientation.z=0.7070
    pose.pose.orientation.w=0.7070
    rospy.loginfo("**Start executeMission"); 
    navigation.gotoPose(pose, 200)        
    navigation.yaw360(commHub.getCurrentPose())
    pose.pose.position.x = -2
    pose.pose.position.y = -2
    pose.pose.position.z = 1
    pose.pose.orientation.x=0
    pose.pose.orientation.y=0
    pose.pose.orientation.z=0
    pose.pose.orientation.w=1
    #navigation.gotoPose(pose, 200)
    #navigation.yaw360(commHub.getCurrentPose())
    pose.pose.position.x = -2
    pose.pose.position.y = 3
    pose.pose.position.z = 2
    pose.pose.orientation.x=0
    pose.pose.orientation.y=0
    pose.pose.orientation.z=-0.7070
    pose.pose.orientation.w=0.7070
    #navigation.gotoPose(pose, 200)
    #navigation.yaw360(commHub.getCurrentPose())
    pose.pose.position.x = 0
    pose.pose.position.y = 0
    pose.pose.position.z = 1
    pose.pose.orientation.x=0
    pose.pose.orientation.y=0
    pose.pose.orientation.z=-1
    pose.pose.orientation.w=0
    navigation.gotoPose(pose, 200)
    navigation.land()
    rospy.loginfo("\t Vehicle armed: %r" % commHub.getCurrentState().armed)
    rospy.loginfo("\t Current mode: %s" %  commHub.getCurrentState().mode)
    rospy.loginfo("\t Vehicle armed: %r" % commHub.getCurrentState().armed)
    rospy.loginfo("\t Current mode: %s" % commHub.getCurrentState().mode)
    rospy.loginfo("landed at: %s " % navigation.strPose(  commHub.getCurrentPose() ))

    rospy.loginfo("**End executeMission")


def main():
    print("Start main")
    try:
        commHub = CommunicationHub() 
        setup(commHub)
        changeOffboardModeAndArm(commHub)
        navigation = Navigation(commHub)
        executeMission(commHub, navigation)
#    except rospy.ROSInterruptException:
#        pass
    except Exception as error:
        rospy.logerr("Caught an exception: "+str(error) + 'Exiting!')
        print ("Caught an exception: "+str(error)+ 'Exiting!')
        quit() 

class CommunicationHub:

    def __init__(self):
        rospy.loginfo("CommunicationHub __init__")
        self.set_mode_client    = rospy.ServiceProxy('mavros/set_mode', SetMode) 
        self.arming_client_cmd  = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
        self.local_pos_pub      = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
        self.land_client        = rospy.ServiceProxy("mavros/cmd/land", CommandTOL)
        self.state_sub          = rospy.Subscriber('mavros/state', State,state_cb) 
        #self.diagnostic          = rospy.Subscriber("diagnostics", DiagnosticArray, diag_cb) 
        self.local_pos_sub      = rospy.Subscriber('mavros/local_position/pose', PoseStamped, pose_cb)
        self.rate = rospy.Rate(20.0);  

    def getCurrentPose(self):
        global current_pose
        return current_pose

    def getCurrentState(self):
        global current_state
        return current_state

if __name__ == '__main__':
    main()

