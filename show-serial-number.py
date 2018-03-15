import getpass
import sys
import telnetlib
import pexpect
import time
import re
import os

HOST = raw_input("Enter terminal server (RPi) IP Address: ")
PORT = raw_input("Enter the telnet port number you are using: ")
#user = raw_input("Enter your telnet username: ")
#password = getpass.getpass()
tn = telnetlib.Telnet(HOST, PORT, timeout = 1)
#tn.set_debuglevel(8)
print "Connecting to " + HOST + " on port " + PORT
tn.write("\r\n")

time.sleep(2)
PRIV = tn.read_eager()
if "#" in PRIV:
	print "Someone Forgot to Logout, Again!"
	tn.write("exit\n")
tn.write("\r\n")
tn.write("\r\n")
hostname = tn.read_until(">", timeout=1).split()[-1]

def ShowVer():
	time.sleep(2)
	tn.write("\r\n")
	tn.write("\r\n")
	print "The Hostname of device is: " + hostname
	tn.write("no\r\n")
	time.sleep(2)
	tn.write("en\r\n")
	time.sleep(2)
	tn.read_until("Router#")
	print "Console Access gained"
	time.sleep(4)
	tn.write("terminal leng 0\n")
	print "Terminal Lenght 0"
	tn.write("show version\n")
	tn.read_eager()
	tn.read_until("Router#")
	time.sleep(4)
	print "show version"
	print tn.read_eager()
	global data
	data = tn.read_until("Router#")
	print "Info collected"
	time.sleep(2)
	tn.write("exit\n")
	print "Exiting...."
	time.sleep(1)
	#tn.write("\x1d")
	#time.sleep(1)
	#tn.write("quit\n")
	#print "Quiting telnet>"
	#time.sleep(1)
	print data
	#tn.set_debuglevel(10)
	#tn.close()

if "#" in hostname:
	print "Someone Forgot to Logout!"
	tn.write("exit\n")
	ShowVer()
else:
	print "All good"
	ShowVer()

p = re.compile('data')

for each_line in data.splitlines():
	if "Linux Software" in each_line:
		global sn
		global mn
		sn = each_line.split()[-4]
		mn = each_line.split()[-6]

print "This is a " + mn + " running software " + sn