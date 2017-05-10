import serial
import array
import time

def send(angle):
	motor = 1
	ser.write(array.array('B',[motor]).tostring())
	# angle = int(raw_input("angle:"))
	ser.write(array.array('B',[angle]).tostring())
	

ser = serial.Serial('/dev/ttyUSB0',9600)

i = 10
flag = 0
delay_time = 1

while(1):
	if (flag == 0) and i < 180:
		print i
		send(i)	
		time.sleep(delay_time)
		i += 15
		
	elif i >= 180:
		flag = 1
		i -= 21
	if (flag == 1) and i > 0:
		print i
		send(i)
		time.sleep(delay_time)
		i -= 15
	elif i <= 0:
		flag = 0
		i += 22
	

	


	
	 
