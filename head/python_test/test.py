import serial
import array


ser = serial.Serial('/dev/ttyUSB0',9600)

while(1):
	motor = int(raw_input("motor:"))
	ser.write(array.array('B',[motor]).tostring())
	angle = int(raw_input("angle:"))
	ser.write(array.array('B',[angle]).tostring())
	
	 
