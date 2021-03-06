#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16, Float32


class RCmaster(object):
    def run(self):
        rate = rospy.Rate(10)  # 10hz
        while not rospy.is_shutdown():
            # Convert (-1.0 -- 1.0) to (-45 -- 45)
            rudderMsg = int(self.rudderPos * 45)
            self.rudderPub.publish(rudderMsg)

            # Convert (-1.0 -- 1.0) to (0 -- 6)
            sailMsg = int((self.sailPos + 1.0) * 6/2.0)
            self.sailPub.publish(sailMsg)

            rospy.loginfo("Sent command (Rudder, Sail)=({}, {})".format(rudderMsg, sailMsg))

            rate.sleep()

    def __init__(self):
        self.rudderPos = 0
        self.sailPos = 0  # TODO: what is the sail neutral pos?

        rospy.init_node('command_center', anonymous=True)
        
        self.rudderPub = rospy.Publisher('rc_mode/rudder/set_point', Int16)
        self.sailPub = rospy.Publisher('rc_mode/sail/set_point', Float32)

        self.sailSub = rospy.Subscriber('rc/sails_in', Float32, self.update_sail)
        self.rudderSub = rospy.Subscriber('rc/rudder_in', Float32, self.update_rudder)

    def update_rudder(self, msg):
        self.rudderPos = msg.data

    def update_sail(self, msg):
        self.sailPos = msg.data


if __name__ == '__main__':
    try:
        core = RCmaster()
        core.run()
    except rospy.ROSInterruptException:
        pass
