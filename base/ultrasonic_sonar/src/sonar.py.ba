#!/usr/bin/env python

import rospy
import serial
import binascii
from sensor_msgs.msg import Range

class Sonar():
    def __init__(self):
        rospy.init_node('sonar_publisher')

        self.rate = rospy.get_param('~rate', 10.0)
        self.device_port = rospy.get_param('~device_port',"/dev/ttyUSB0")
        self.frame_id = rospy.get_param('~sonar_frame_id', '/sonar')
        self.field_of_view = rospy.get_param('~field_of_view', 0.1)
        self.min_range = rospy.get_param('~min_range', 0.02)
        self.max_range = rospy.get_param('~max_range', 4.50)
        self.sonar_pub = rospy.Publisher('/sonar', Range, queue_size=50)
        self.ser = serial.Serial(self.device_port, 9600, timeout=1)

    def handleSonar(self):
        sonar = Range()
        sonar.header.frame_id = self.frame_id
        sonar.radiation_type = Range.ULTRASOUND
        sonar.field_of_view = 0.1
        sonar.min_range = self.min_range
        sonar.max_range = self.max_range
        self.ser.write(binascii.a2b_hex('55')) ##modify as your UART command 
        line = self.ser.readline()
        try:
            high = ord(line[0])
            low = ord(line[1])
            distance = (high*256. + low)/1000.
        except:
            distance = 11.
        # print distance,'m'
        # print ":".join("{:02x}".format(ord(c)) for c in line)
        sonar.header.stamp =  rospy.Time.now()
        sonar.range = distance

        self.sonar_pub.publish(sonar)

    def spin(self):
        r = rospy.Rate(self.rate)
        while not rospy.is_shutdown():
            self.handleSonar()
            r.sleep()

if __name__ == '__main__':
    scanner = Sonar()
    rospy.loginfo("=== run")
    scanner.spin()
    rospy.loginfo("=== end")
