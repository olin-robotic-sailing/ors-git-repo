#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16, Float32

class autonomousRudderPublisher:#needs a topic to read in waypoint angle from
	def __init__(self):
		rospy.init_node('rudder_publisher')
		self.rudderPub = rospy.Publisher('auto_mode/rudder/set_point', Int16)
		self.waypoint = 0
		def callback(angle):
			self.waypoint = angle.data
		self.waypointAngleListener = rospy.Subscriber('heading_err', Int16, callback) #needs somewhere to get waypoint
	def calculateRudderPosition(self, waypointAngle):#calculate position rudder needs to be at to direct self at current waypoint angle, relative to bow of the boat as 0 degrees, positive is starboard and negative is port
		#currently nobody has defined rudder controls
		#rudder messages currently range from -45 to 45, assuming positive is starboard and negative is port
		turnAngle = waypointAngle / 2 if abs(waypointAngle) < 90 else 45 if(waypointAngle > 0) else -45 #need information on how much exactly a rudder should be turned
		return turnAngle

	def run(self):
		rate = rospy.Rate(10)  # 10hz
		while not rospy.is_shutdown():
			rud = self.calculateRudderPosition(self.waypoint)
			self.rudderPub.publish(rud)
			rospy.loginfo("Sent desired rudder angle : {}".format(rud))
			rate.sleep()

if __name__ == '__main__':
	try:
		test = autonomousRudderPublisher()
		test.run()
	except rospy.ROSInterruptException:
		pass
