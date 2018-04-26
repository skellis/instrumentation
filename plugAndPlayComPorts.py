"""

.. module: plugAndPlayCompports
   :platform: Windows
.. moduleauthor:: Scott R. Ellis <skellis@berkeley.edu>

 plugAndPlayComports.py is a simple utility function that automatically detects and connects to a communication RS232 port by querying all 
 the Com port with a readString and connecting to the one that returns a writeString. It uses both pyvisa and pyserial. You will want to download
 these modules. I recommend get_pip.py and invoking the commands:
 python -m pip install pyserial
 python -m pip install pyvisa

"""

import visa
import serial
import unicodedata




def plugAndPlayComPorts(writeString,readString,timeoutx=0.1,baudratex=9600,readbytes=10000):
	counter=0
	comPortNames=""
	desiredName=""
	desiredOutput=""
	found=0
	rm = visa.ResourceManager()
	comres = rm.list_resources()
	comres_info = rm.list_resources_info()
	for d in comres:
		tempUnicodePort= comres_info[d].alias
		tempPortName=unicodedata.normalize('NFKD', tempUnicodePort).encode('ascii','ignore')
		comPortNames+=tempPortName+";"
		counter+=1
		ser = serial.Serial()
		ser.port= tempPortName
		ser.timeout=timeoutx
		ser.baudrate=baudratex
		ser.open()
		ser.write(writeString)
		ser.flush
		output=ser.read(readbytes).lower()
		ser.close()
		if output.find(readString) != -1:
			found = 1
			desiredOutput=output
			desiredPort=d
			desiredName=tempPortName
	print str(counter)+" Com ports were detected."
	if counter>0:
		print comPortNames
		if found:
			print "Your instrument returned: "+desiredOutput
			print "The port you are looking for is "+desiredName
			print "You connected automatically."	
			return desiredPort
		else:
			print "The port you were looking for was not found. You could consider changing the number of bites read, the default baud rate or the time out time"
	return ""

readString="oregon"
writeString ="WQ;WY;"
plugAndPlayComPorts(writeString,readString)
