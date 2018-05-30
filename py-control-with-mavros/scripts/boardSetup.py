import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State 
#def state_cb(state):
#    global current_state
#    current_state = state

local_pos_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
#state_sub = rospy.Subscriber('mavros/state', State, state_cb)

# define some functions
def printhello():
    print "hello"
    
def timesfour(input):
    print input * 4
    
