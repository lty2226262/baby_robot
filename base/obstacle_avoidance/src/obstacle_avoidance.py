#!/usr/bin/python
import rospy
import roslib

# Messages
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import Range

class CmdVelWatchDog:
	def __init__(self):
		rospy.init_node('obstacle_avoidance')

		self.rate = rospy.get_param('~rate',100)
		self.tolerance_fore = rospy.get_param('~tolerance_fore',0.20)
		self.tolerance_back = rospy.get_param('~tolerance_back',0.20)
		self.sonar_fore = rospy.get_param('~sonar_fore','/fore/sonar')
		self.sonar_back = rospy.get_param('~sonar_back','/back/sonar')

		self.target_v = 0.
		self.target_w = 0.
		self.sonar_fore_distance = 99.
		self.sonar_back_distance = 99.

		self.cmd_vel_sub = rospy.Subscriber('cmd_vel', Twist, self.twistCallback)
		self.FORE = 0
		self.BACK = 1
		self.sonar_fore_sub = rospy.Subscriber(self.sonar_fore, Range, self.rangeCallback,self.FORE)
		self.sonar_back_sub = rospy.Subscriber(self.sonar_back, Range, self.rangeCallback,self.BACK)

		self.cmd_vel_pub = rospy.Publisher('cmd_vel',Twist, queue_size = 1)

	def twistCallback(self, msg):
		self.target_v = msg.linear.x
		self.target_w = msg.linear.z

	def rangeCallback(self, msg, direction):
		if (direction == self.FORE):
			self.sonar_fore_distance = msg.range
		elif (direction == self.BACK):
			self.sonar_back_distance = msg.range
		else:
			print 'SOMETHING WRONG WITH THE FLAG!'

	def update(self):
		if (self.sonar_fore_distance < self.tolerance_fore) and (self.target_v > 0):
			self.target_v = 0.
			self.cmd_vel_pub.publish(Twist(Vector3(self.target_v,0.,0.), Vector3(0.,0.,self.target_w)))
			rospy.logwarn("FRONT HITS WALL!")
		elif (self.sonar_back_distance < self.tolerance_back) and (self.target_v < 0):
			self.target_v = 0.
			self.cmd_vel_pub.publish(Twist(Vector3(self.target_v,0.,0.), Vector3(0.,0.,self.target_w)))
			rospy.logwarn("FRONT HITS WALL!")

	def shutdown(self):
	    rospy.loginfo("Stop diffdrive_controller")
	  	# Stop message
	    rospy.sleep(1)  

	def spin(self):
		rate = rospy.Rate(self.rate)
		rospy.on_shutdown(self.shutdown)

		while not rospy.is_shutdown():
			self.update()

def main():
	cmd_vel_watchdog = CmdVelWatchDog()
	cmd_vel_watchdog.spin()

if __name__ == '__main__':
	main()
