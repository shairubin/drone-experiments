import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State 
from mavros_msgs.srv import SetMode, CommandBool, CommandTOL


# callback method for state sub
current_state = State() 
offb_set_mode = SetMode # more about px4 modes: https://dev.px4.io/en/concept/flight_modes.html 
def state_cb(state):
    global current_state
    current_state = state

 
state_sub = rospy.Subscriber('mavros/state', State, state_cb)
arming_client_cmd = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
local_pos_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
land_client = rospy.ServiceProxy("mavros/cmd/land", CommandTOL)
set_mode_client = rospy.ServiceProxy('mavros/set_mode', SetMode) 

#rospy.init_node('offb_node', anonymous=True) 

# define some functions
def printhello():
    print "hello"
    
def timesfour(input):
    print input * 4
    
