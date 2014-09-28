#!/usr/bin/python

import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=60)
logfile = open('/dylos/test.csv', 'a')
while True:
        line = ser.readline()
        now = time.strftime("%Y-%m-%d,%H:%M:%S", time.localtime())
        a =  "%s,%s" % (now,line)
        print a
        logfile.write(a)
        logfile.flush()
logfile.close()
ser.close()

