#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import serial
import array

g_ip_address = '192.168.192.168'
g_serial_port = '/dev/ttyUSB0'

class RobotHead:
    def __init__(self):
        # Initialize the serial
        self.this_serial = serial.Serial(g_serial_port, 9600)
        # Initialize the web port
        self.this_ip = g_ip_address
        self.this_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.this_socket.bind((self.this_ip, 9999))
        self.absolute_angle = 90
        self.is_rotate = True
        self.RotateTo(90)
        print 'Initialization complete'

    def ReceiveData(self):
        data, address = self.this_socket.recvfrom(1024)
        print 'Received from %s:%s.' % address
        print data
        try:
        	angle = int(data)
        except:
            angle = 315
            print 'invalid data from client#############'
        return angle

    def AngleTransform(self,in_angle):
        if (in_angle > 135):
            angle = in_angle -360
        else:
            angle = in_angle
        rotate_angle = angle + 45
        print 'rotate angle', rotate_angle
        rotate_angle *= 1.5
        print 'after augument', rotate_angle
        send_angle = self.absolute_angle - int(rotate_angle)
        if send_angle < 0:
            send_angle = 0
        elif send_angle > 180:
            send_angle = 180
        if abs(send_angle - self.absolute_angle) > 10:
            self.absolute_angle = send_angle
            self.is_rotate = True
        print self.absolute_angle
        return self.absolute_angle

    def RotateTo(self,angle):
        if (self.is_rotate == True):
            self.this_serial.write(array.array('B', [1]).tostring())
            self.this_serial.write(array.array('B', [angle]).tostring())
            self.is_rotate = False

if __name__ == "__main__":

    server = RobotHead()

    while True:
        receive_angle = server.ReceiveData()
        pocessed_angle = server.AngleTransform(receive_angle)
        server.RotateTo(pocessed_angle)
