# instrumentation

 plugAndPlayComports.py is a simple utility function that automatically detects and connects to a communication RS232 port by querying all 
 the Com port with a readString and connecting to the one that returns a writeString. It uses both pyvisa and pyserial. You will want to download
 these modules. I recommend get_pip.py and invoking the commands:
 python -m pip install pyserial
 python -m pip install pyvisa
 