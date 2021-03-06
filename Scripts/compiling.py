import os
import time
import urllib
import urllib2
import subprocess
from subprocess import call
import RPi.GPIO as gpio

#=========================================================================

#message = input("Enter Message :")
message = 'System Started'
#number = input("Enter reciever phone number :")
number = '9873707004'
flag1=100
flag2=100
flag3=100
flag4=100
count=0
#=========================================================================
def sendSMS(uname, hashCode, numbers, sender, message):
	data =  urllib.urlencode({'username': uname, 'hash': hashCode, 'numbers': numbers, 'message' : message, 'sender': sender})
	data = data.encode('utf-8')
	request = urllib2.Request("http://api.textlocal.in/send/?")
	f = urllib2.urlopen(request, data)#I need to use urllib2 and urllib because urlopen in urllib2 can take a request class but urllib does not include a function like urlencode.
	fr = f.read()
    	return(fr)
#=========================================================================
def sw1_detect(pin):#switch for water logging
	print 'Water Logging Detected'
	gpio.remove_event_detect(19)#The water sensor is connected to the general purpose I/O pin 19
	global flag1
	if (flag1==100):
		flag1=0
		subprocess.call("./save1.sh", shell=False)
		print('W button inactive')
		resp =  sendSMS('bishan@gmail.com', 'satnamWAHEGURU123', number, 'Water Logging Detected', 'TXTLCL')
		print (resp)

#=========================================================================
def sw2_detect(pin):
	print 'Panic Button Detected'
	gpio.remove_event_detect(11)
	global flag2
	if (flag2==100):
		flag2=0
		subprocess.call("./save2.sh", shell=False)
		print('P button inactive')
		resp =  sendSMS('bishan@bm-es.com', 'satnamWAHEGURU123', number, 'TXTLCL', 'Panic Button Detected')
		print (resp)
#=========================================================================
def sw3_detect(pin):
	print 'Traffic Light Crossing Detected'
	global count
	if count>=6 and count<=12 :#red light 6 to 12 seconds 
		gpio.remove_event_detect(12)
		global flag3
		if (flag3==100):
			flag3=0
			subprocess.call("./save3.sh", shell=False)
			print('T button inactive')
			resp =  sendSMS('bishan@bm-es.com', 'satnamWAHEGURU123', number, 'TXTLCL', 'Light Crossing Detected')
			print (resp)
#=========================================================================
def sw4_detect(pin):
	print 'Image Saving Detected'
	gpio.remove_event_detect(7)
	global flag4
	if (flag4==100):
		flag4=0
		subprocess.call("./save4.sh", shell=False)
		print('I inactive')
#=========================================================================
def red_on():
	print 'Red On'
#=========================================================================
def green_on():
	print 'Green On'
#=========================================================================
def init_io():
	gpio.setmode(gpio.BOARD) # Set pin numbering to board numbering
	gpio.setwarnings(False)
	gpio.setup(7, gpio.IN) # Set up pin 7 as an input for 1 minute
	gpio.add_event_detect(7, gpio.RISING, callback=sw4_detect, bouncetime=200) # Set up an interrupt to look for button presses
	gpio.setup(11, gpio.IN) # Set up pin 11 as an input for panic
	gpio.add_event_detect(11, gpio.RISING, callback=sw2_detect, bouncetime=200) # Set up an interrupt to look for button presses
	gpio.setup(12, gpio.IN) # Set up pin 12 as an input for traffic
	gpio.add_event_detect(12, gpio.FALLING, callback=sw3_detect, bouncetime=200) # Set up an interrupt to look for button presses
	gpio.setup(19, gpio.IN) # Set up pin 7 as an input
	gpio.add_event_detect(19, gpio.RISING, callback=sw1_detect, bouncetime=200) # Set up an interrupt to look for button presses
	
	
	gpio.setup(13, gpio.IN) # Set up pin 13 as an input for 
	#gpio.add_event_detect(13, gpio.RISING, callback=sw4_detect, bouncetime=200) # Set up an interrupt to look for button presses
	gpio.setup(15, gpio.IN) # Set up pin 15 as an input
	#gpio.add_event_detect(15, gpio.RISING, callback=sw5_detect, bouncetime=200) # Set up an interrupt to look for button presses
	
	
	gpio.setup(22, gpio.OUT) # Set up pin 22 as an output pin for 1 minute capture
	gpio.output(22, False)
	
	gpio.setup(16, gpio.OUT) # Set up pin 16 as an output red color
	gpio.output(16, False)
	gpio.setup(18, gpio.OUT) # Set up pin 18 as an output green color
	gpio.output(18, True)



	if (gpio.input(13) == True): # Physically read the pin now
		print('13 High')
	else:
		print('13 Low')

	if (gpio.input(15) == True): # Physically read the pin now
		print('15 High')
	else:
		print('15 Low')
