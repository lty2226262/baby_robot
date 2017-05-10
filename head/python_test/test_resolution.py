import serial
import array
import time

def send(angle):
	motor = 1
	ser.write(array.array('B',[motor]).tostring())
	ser.write(array.array('B',[angle]).tostring())
	

ser = serial.Serial('/dev/ttyUSB0',9600)

send(60)

resolution = int(raw_input("resolution:"))
ser.write(array.array('B',[4]).tostring())
ser.write(array.array('B',[resolution]).tostring())	

send(120)


	
	 
