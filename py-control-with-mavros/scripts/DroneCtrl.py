import rospy
import boardSetup
from geometry_msgs.msg import PoseStamped


class DroneCtrl:
	pose = PoseStamped()
	pose.pose.position.x = 0
	pose.pose.position.y = 0
	pose.pose.position.z = 2

	
	def setup(self, rate): 
		print('setup')	
		rospy.loginfo("Start changeOffboardModeAndArm"); 
 #    	# send a few setpoints before starting
 		rospy.loginfo('send a few setpoints before starting')
 		for i in range(100):
 			boardSetup.local_pos_pub.publish(self.pose)
			rate.sleep()

 		rospy.loginfo('wait for FCU connection')    
 #    	# wait for FCU connection
 		while not boardSetup.current_state.connected:
			rate.sleep()
    
 		rospy.loginfo('FCU connected !')    

