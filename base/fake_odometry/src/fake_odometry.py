#!/usr/bin/env python
import roslib
roslib.load_manifest('differential_control')
import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion

if __name__ == '__main__':
    rospy.init_node('fake_odometry')
    base_frame_id = 'base_link'
    odom_frame_id = 'odom'
    rate_value = 0.75

    odom_pub = rospy.Publisher("odom", Odometry, queue_size=5)
    odom_broadcaster = tf.TransformBroadcaster()
    listener = tf.TransformListener()
    last_position_x = 0.0
    last_position_y = 0.0
    last_angular_z = 0.0
    last_angular_w = 1.0
    last_angular_theta = 0.0

    now_position_x = 0.0
    now_position_y = 0.0
    now_angular_z = 0.0
    now_angular_w = 1.0
    now_angular_theta = 0.0

    dx = 0.0
    dz = 0.0

    then = rospy.Time.now()

    rate = rospy.Rate(rate_value)
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('odom', 'laser', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        now = rospy.Time.now()
	# print now
        elapsed = now - then
	# print elapsed
        elapsed = elapsed.to_sec()

        now_position_x = trans[0]
        now_position_y = trans[1]
        now_angular_z = rot[2]
        now_angular_w = rot[3]
        now_angular_theta = math.atan2(now_angular_z, now_angular_w) * 2.0

        if elapsed > 0:
            dx = (math.sqrt((now_position_x - last_position_x) ** 2 + (now_position_y - last_position_y) ** 2))/elapsed
            dz = (now_angular_theta - last_angular_theta) / elapsed
        else:
            dx = 0.0
            dz = 0.0

        print "dx:",dx,"dz:",dz,"elapsed",elapsed

        odom_broadcaster.sendTransform(trans,
            rot,
            now,
            base_frame_id,
            odom_frame_id
            )

        last_position_x = now_position_x
        last_position_y = now_position_y
        last_angular_z = now_angular_z
        last_angular_w = now_angular_w
        last_angular_theta = now_angular_theta
        then = now

        quaternion = Quaternion()
        quaternion.x = rot[0]
        quaternion.y = rot[1]
        quaternion.z = rot[2]
        quaternion.w = rot[3]
        odom = Odometry()
        odom.header.stamp = now
        odom.header.frame_id = odom_frame_id
        odom.pose.pose.position.x = trans[0]
        odom.pose.pose.position.y = trans[1]
        odom.pose.pose.position.z = trans[2]
        odom.pose.pose.orientation = quaternion
        odom.child_frame_id = base_frame_id
        odom.twist.twist.linear.x = dx
        odom.twist.twist.linear.y = 0
        odom.twist.twist.angular.z = dz
        # print odom
        odom_pub.publish(odom)

        rate.sleep()
