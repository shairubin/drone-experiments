#!/usr/bin/env python
#import rospy
# import mavros
# import mavros_msgs
# import copy 
#import pprint
# from geometry_msgs.msg import PoseStamped
#from mavros_msgs.msg import State 
# from mavros_msgs.srv import SetMode, CommandBool, CommandTOL
# from tf.transformations import quaternion_from_euler

#current_state = State() 

#def state_cb(state):    # when state changed this function will be called 
#    global current_state
#    rospy.loginfo("State callback function!")
#    current_state = state
#    rospy.loginfo(pprint.pformat(state))


# class CommunicationHub:


#     def __init__(self):
#         rospy.loginfo("CommunicationHub __init__")
#         self.set_mode_client    = rospy.ServiceProxy('mavros/set_mode', SetMode) 
#         self.arming_client_cmd  = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
#         self.local_pos_pub      = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
#         self.land_client        = rospy.ServiceProxy("mavros/cmd/land", CommandTOL)
#         self.state_sub          = rospy.Subscriber('mavros/state', State, state_cb) # used in setup of drneCtrl 
#         self.rate = rospy.Rate(20.0)
        
        

