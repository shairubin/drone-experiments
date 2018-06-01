import rospy
import pprint 
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State 
from mavros_msgs.srv import SetMode, CommandBool, CommandTOL


# callback method for state sub
current_state = State() 
offb_set_mode = SetMode # more about px4 modes: https://dev.px4.io/en/concept/flight_modes.html 
def state_cb(state):  # when state changed this function will be called 
    global current_state
    rospy.logdebug("State callback function!")
    current_state = state
    rospy.logdebug(pprint.pformat(state))
 
state_sub = rospy.Subscriber('mavros/state', State, state_cb) # used in setup of drneCtrl 
arming_client_cmd = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
local_pos_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
land_client = rospy.ServiceProxy("mavros/cmd/land", CommandTOL)
#class modeSetup:
set_mode_client = rospy.ServiceProxy('mavros/set_mode', SetMode) 
def setOffBaord():
    set_mode_client(base_mode=0, custom_mode="OFFBOARD")

