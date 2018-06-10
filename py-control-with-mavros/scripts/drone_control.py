#!/usr/bin/env python
import rospy
from tf.transformations import quaternion_from_euler, euler_from_quaternion
import math

class Navigation:
    def __init__(self):
        rospy.loginfo("Navigation __init__")  

    def gotoPose(self, pose, commHub, duration):
        rospy.loginfo("**Start gotoPose: %s", self.strPose(pose)) 
        loops =0    
        while (not rospy.is_shutdown() and loops< duration):
            loops +=1;  
            # Update timestamp and publish pose 
            pose.header.stamp = rospy.Time.now()
            commHub.local_pos_pub.publish(pose)
            commHub.rate.sleep()
        
        rospy.loginfo("**End   gotoPose: %s", self.strPose(commHub.getCurrentPose()))
    
    
    def yaw360(self, startPose, commHub):
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
            self.gotoPose(nextPose,commHub ,delay)    
        rospy.loginfo("**End yaw360: %s", self.strPose(commHub.getCurrentPose())) 
 


    def strPose(self, pose):
        return str([round(pose.pose.position.x,2), round(pose.pose.position.y,2), round(pose.pose.position.z,2), \
                    round(pose.pose.orientation.x,2), round(pose.pose.orientation.y,2), round(pose.pose.orientation.z,2), \
                    round(pose.pose.orientation.w,2)])    
