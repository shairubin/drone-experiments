import rospy
import boardSetup
from geometry_msgs.msg import PoseStamped


class DroneCtrl:
	startPose = PoseStamped()
	startPose.pose.position.x = 0
	startPose.pose.position.y = 0
	startPose.pose.position.z = 2

	
	def setup(self, rate): 
		print('setup')	
		rospy.loginfo("Start changeOffboardModeAndArm"); 
 #    	# send a few setpoints before starting
 		rospy.loginfo('send a few setpoints before starting')
 		for i in range(100):
 			boardSetup.local_pos_pub.publish(self.startPose)
			rate.sleep()

 		rospy.loginfo('wait for FCU connection')    
 #    	# wait for FCU connection
 		while not boardSetup.current_state.connected:
			rate.sleep()
    
 		rospy.loginfo('FCU connected !')    

	def changeOffboardModeAndArm(self, currentRate, my_set_mode_client):
		prev_state = boardSetup.current_state 
		last_request = rospy.get_rostime()
		duration = rospy.Duration(5.)
		loops =0; 
		while (not rospy.is_shutdown() and boardSetup.current_state.armed == False): 
			currentRate.sleep()
			loops+=1
			now = rospy.get_rostime()
			if (loops % 30 ==0 ):
				rospy.loginfo("Current mode: %s " %boardSetup.current_state.mode)
				rospy.loginfo("Current loops: %d " %loops)
			
			if boardSetup.current_state.mode != "OFFBOARD" and (now - last_request > duration):
				rospy.loginfo('setting mode to OFFBOARD')
				my_set_mode_client(base_mode=0, custom_mode="OFFBOARD")
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
        	#currentRate.sleep()

		rospy.loginfo("\t Vehicle armed: %r" % boardSetup.current_state.armed)
		rospy.loginfo("\t Current mode: %s" % boardSetup.current_state.mode)
		rospy.loginfo("End changeOffboardModeAndArm with %d iterations" %loops); 


