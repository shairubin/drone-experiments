#!/usr/bin/env python
import rospy
from tf.transformations import quaternion_from_euler, euler_from_quaternion
import math
"""
This  module implements compund control actions to the drone.
To generate HTML documentation for this module issue the
command:

    pydoc -w  <file name>
"""
class Navigation:
    def __init__(self, commHub_in):
        rospy.loginfo("Navigation __init__") 
        self.commHub = commHub_in 

    def gotoPose(self, pose, duration):
        """
        pose: target position
        commHub: CommunicationHub class to communicate with the drone
        duration: counter for the duration of the operation 
    
        TODO:  ducation and commHub should be eliminated from class description 
        """
        rospy.loginfo("**Start gotoPose: %s", self.strPose(pose)) 
        loops =0    
        while (not rospy.is_shutdown() and loops< duration):
            loops +=1;  
            # Update timestamp and publish pose 
            pose.header.stamp = rospy.Time.now()
            self.commHub.local_pos_pub.publish(pose)
            self.commHub.rate.sleep()
        
        rospy.loginfo("**End   gotoPose: %s", self.strPose(self.commHub.getCurrentPose()))
    
    
    def yaw360(self, startPose):
        nSteps = 30
        delay = 10
        rospy.loginfo("**Start yaw360: %s", self.strPose(startPose)) 
        q = quaternion_from_euler(0, 0, -3.14)
        #print "The quaternion representation is %s %s %s %s." % (q[0], q[1], q[2], q[3])
        q = [startPose.pose.orientation.x, startPose.pose.orientation.y, startPose.pose.orientation.z, startPose.pose.orientation.w] 
        ePose = list(euler_from_quaternion(q)) 
        rospy.loginfo("Start ePose: %s", str(ePose))
        nextPose = startPose
        step = (2.0*math.pi)/nSteps
        for i in range(1,nSteps):
            ePose[2] +=  step     
            rospy.logdebug("next ePose: %s", str(ePose))
            q = quaternion_from_euler(ePose[0], ePose[1],ePose[2])
            nextPose.pose.orientation.z = q[2]
            nextPose.pose.orientation.w = q[3]
            rospy.logdebug("Pose step %d: %s",i, self.strPose(nextPose))
            self.gotoPose(nextPose ,delay)    
        rospy.loginfo("**End yaw360: %s", self.strPose(self.commHub.getCurrentPose())) 
 

    def land(self):

        rospy.loginfo("trying to land");
    # landing procedure -- send land messages until successfull command 
        land_response = self.commHub.land_client(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
        loops = 0
        while (land_response.success == False and loops < 200):
          loops+=1 
          if (loops % 50 == 0):
            rospy.loginfo("sending landing command again, Counter: %d" , loops)
          land_response = self.commHub.land_client(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
          self.commHub.rate.sleep()
    # wait for engines to stop 
        if (loops == 200):
            rospy.logerr("Cannot land!")
        
        while (self.commHub.getCurrentState().armed == True):
            self.commHub.rate.sleep()

    def strPose(self, pose):
        return str([round(pose.pose.position.x,2), round(pose.pose.position.y,2), round(pose.pose.position.z,2), \
                    round(pose.pose.orientation.x,2), round(pose.pose.orientation.y,2), round(pose.pose.orientation.z,2), \
                    round(pose.pose.orientation.w,2)])    
