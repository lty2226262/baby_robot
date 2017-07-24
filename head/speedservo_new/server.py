#!/usr/bin/env python
# -*- coding: utf-8 -*-

import array
from time import sleep
DEBUG = False
INPUT_DEBUG = False

if not DEBUG:
    import socket
    import serial
    g_ip_address = '192.168.192.168'
    g_serial_port = '/dev/ttyUSB0'
else:
    import matplotlib.pyplot as plt


class RobotHead:
    def __init__(self):
        if not DEBUG:
            # Initialize the serial
            self.this_serial = serial.Serial(g_serial_port, 9600)
            # Initialize the web port
            self.this_ip = g_ip_address
            self.this_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.this_socket.bind((self.this_ip, 9999))
        self.pitch = 102
        self.roll = 90
        self.absolute_angle = 90
        self.pre_angle = 90
        self.is_rotate = True
        self.path = []
        self.flexible = []
        self.accelerate_limit = 0.2
        self.move_delay_max = 20.0
        self.move_delay_min = 6.0
        self.RotateTo(90)
        print 'Initialization complete'

    def ReceiveData(self):
        if not DEBUG and (not INPUT_DEBUG):
            data, address = self.this_socket.recvfrom(1024)
            print 'Received from %s:%s.' % address
            print data
        else:
            data = raw_input("please_input_a_detect_angle")
        if INPUT_DEBUG:
            data = raw_input("please_input_a_detect_angle")
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
        rotate_angle *= 1.0
        print 'after augument', rotate_angle
        send_angle = self.absolute_angle - int(rotate_angle)
        if send_angle < 0:
            send_angle = 0
        elif send_angle > 180:
            send_angle = 180
        if abs(send_angle - self.absolute_angle) > 10:
            self.pre_angle = self.absolute_angle
            self.absolute_angle = send_angle
            self.is_rotate = True
        print self.absolute_angle
        return self.absolute_angle

    def ComputePath(self,current,target):
        self.path = []
        self.flexible = []
        for i in range(abs(current -target) + 1):
            self.path.append(1.0)
            self.flexible.append(1)
        if len(self.path) > 3:
            for i in (0,1,-2,-1):
                self.flexible[i] = 0
        else:
            return
        mid_index = int(len(self.path) / 2)
        mid_value = 1.0 - float(mid_index) * self.accelerate_limit / self.move_delay_max
        if mid_value < self.move_delay_min / self.move_delay_max :
            min_index = int((self.move_delay_max - self.move_delay_min) / self.accelerate_limit)
            for i in range(min_index, len(self.path) - min_index):
                self.path[i] = self.move_delay_min / self.move_delay_max
                self.flexible[i] = 0
        else:
            self.path[mid_index] = mid_value
            self.flexible[mid_index] = 0
        self.Smooth()
        # if DEBUG == True:
        #     print self.path
        #     print self.flexible

    def Smooth(self):
        tolerance = 0.001
        weight_smooth = 0.3
        error = tolerance
        while error >= tolerance:
            error = 0.0
            for i in range(len(self.path)):
                if self.flexible[i] == 1:
                    aux = self.path[i]
                    self.path[i] += (weight_smooth * (self.path[i - 1] + self.path[i + 1] - 2 * self.path[i]) +
                                    (weight_smooth / 2) * (2 * self.path[i - 1] - self.path[i - 2] - self.path[i]) +
                                    (weight_smooth / 2) * (2 * self.path[i + 1] - self.path[i + 2] - self.path[i]))
                    error += abs(self.path[i] - aux)
        # if DEBUG == True:
        #     speed = [1.0/n for n in self.path]
        #     x = [n for n in range(len(self.path))]
        #     # plt.plot(x, speed)
        #     # plt.show()

    def RotateTo(self,angle):
        self.ComputePath(self.pre_angle, self.absolute_angle)
        if self.is_rotate:
            if self.absolute_angle - self.pre_angle > 0:
                sign = 1
            elif self.absolute_angle - self.pre_angle < 0:
                sign = -1
            else:
                sign = 0
            if not DEBUG:
                for i in range(abs(self.absolute_angle - self.pre_angle) + 1):
                    angle = self.pre_angle + sign * i
                    if angle != self.absolute_angle:
                        stop_bit = 0
                    else:
                        stop_bit = 1
                    self.this_serial.write(array.array('B', [170]).tostring())
                    self.this_serial.write(array.array('B', [angle]).tostring())
                    self.this_serial.write(array.array('B', [self.pitch]).tostring())
                    self.this_serial.write(array.array('B', [self.roll]).tostring())
                    self.this_serial.write(array.array('B', [stop_bit]).tostring())
                    self.this_serial.write(array.array('B', [85]).tostring())
                    sleep(float(self.path[i]) * self.move_delay_max / 1000)
            else:
                for i in range(abs(self.absolute_angle - self.pre_angle) + 1):
                    angle = self.pre_angle + sign * i
                    if angle != self.absolute_angle:
                        stop_bit = 0
                    else:
                        stop_bit = 1
                    print [170, angle, self.pitch, self.roll, stop_bit, 85], " wait: ",\
                        float(self.path[i]) * self.move_delay_max / 1000
                    sleep(float(self.path[i]) * self.move_delay_max / 1000)
            self.is_rotate = False


if __name__ == "__main__":

    server = RobotHead()

    while True:
        receive_angle = server.ReceiveData()
        pocessed_angle = server.AngleTransform(receive_angle)
        server.RotateTo(pocessed_angle)
