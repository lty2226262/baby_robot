#!/usr/bin/python
import rospy
import roslib
import serial
import binascii

# Messages
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

class CmdVelToDiffDriveMotors:
  def __init__(self):
    rospy.init_node('diffdrive_controller')
    self.cmdvel_sub = rospy.Subscriber('/cmd_vel', Twist, self.twistCallback)
    self.lwheel_tangent_vel_target_pub = rospy.Publisher('lwheel_tangent_vel_target', Float32, queue_size=10)
    self.rwheel_tangent_vel_target_pub = rospy.Publisher('rwheel_tangent_vel_target', Float32, queue_size=10)

    self.L = rospy.get_param('~robot_wheel_separation_distance', 0.24) 

    self.rate = rospy.get_param('~rate', 1)
    self.timeout_idle = rospy.get_param('~timeout_idle', 2)
    self.time_prev_update = rospy.Time.now()
    self.default_vel = rospy.get_param('~default_vel', 0.4)
    self.vel_scale = rospy.get_param('~vel_scale',254)
    self.device_port = rospy.get_param('~device_port',"/dev/ttyUSB1")

    self.target_v = 0
    self.target_w = 0
    
    try:
      self.ser = serial.Serial(self.device_port, 115200)
    except:
      rospy.logerr("No serial device")

  def sendBags(self, left, right):
    if left > 0:
      signal_left = 1
    else:
      signal_left = 0
      left = -left
    if right > 0:
      signal_right = 1
    else:
      signal_right = 0
      right = -right
    if left > 254:
      left = 254
      rospy.loginfo("LEFT WHEEL SPEED OUT OF LIMIT")
    if right > 254:
      right = 254
      rospy.loginfo("RIGHT WHEEL SPEED OUT OF LIMIT")
    send = 'ff'
    send += 'ff'
    send += ' ' + "{:02x}".format(signal_left)
    send += ' ' + "{:02x}".format(left)
    send += ' ' + "{:02x}".format(signal_right)
    send += ' ' + "{:02x}".format(right)
    send += ' ' + '0d'
    send += ' ' + '0a'
    # rospy.loginfo("SENDING BAGS is : %s", send)
    
    sendHex = send.split()
    for i in range(len(sendHex)):
      sendHex[i] = binascii.a2b_hex(sendHex[i])
      try:
        self.ser.write(sendHex[i])    
      except:
        rospy.logerr("No serial device!!")


  def velocityRemap(self, vel):
    return int(vel / self.default_vel * self.vel_scale)

  # When given no commands for some time, do not move


  def spin(self):
    rospy.loginfo("Start diffdrive_controller")
    rate = rospy.Rate(self.rate)
    time_curr_update = rospy.Time.now()
    
    rospy.on_shutdown(self.shutdown)

    while not rospy.is_shutdown():
      time_diff_update = (time_curr_update - self.time_prev_update).to_sec()
      if time_diff_update < self.timeout_idle: # Only move if command given recently
        self.update();
      rate.sleep()
    rospy.spin();

  def shutdown(self):
    rospy.loginfo("Stop diffdrive_controller")
  	# Stop message
    self.lwheel_tangent_vel_target_pub.publish(0)
    self.rwheel_tangent_vel_target_pub.publish(0)
    rospy.sleep(1)    

  def update(self):
    # Suppose we have a target velocity v and angular velocity w
    # Suppose we have a robot with wheel radius R and distance between wheels L
    # Let vr and vl be angular wheel velocity for right and left wheels, respectively
    # Relate 2v = R (vr +vl) because the forward speed is the sum of the combined wheel velocities
    # Relate Lw = R (vr - vl) because rotation is a function of counter-clockwise wheel speeds
    # Compute vr = (2v + wL) / 2R
    # Compute vl = (2v - wL) / 2R
    vr = self.velocityRemap(2*self.target_v + self.target_w*self.L) / (2)
    vl = self.velocityRemap(2*self.target_v - self.target_w*self.L) / (2)
    
    self.sendBags(vr,vl)

    self.rwheel_tangent_vel_target_pub.publish(vr)
    self.lwheel_tangent_vel_target_pub.publish(vl)

  def twistCallback(self,msg):
    self.target_v = msg.linear.x;
    self.target_w = msg.angular.z;
    self.time_prev_update = rospy.Time.now()


def main():
  cmdvel_to_motors = CmdVelToDiffDriveMotors();
  cmdvel_to_motors.spin()

if __name__ == '__main__':
  main(); 
