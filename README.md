Dylos DC1100 Pro to InfluxDB + Grafana
======================================

The Dylos DC1100 Pro is an air quality monitor that is capable of
measuring particles between 0.5 and 2.5 micron and between 2.5 and 10 micron.

The measured values as displayed on the device are in parts per 0.01 cubic feet.
This particular model has a serial port that outputs the average values per minute.

The format of this output is 0.5<2.5 micron,>2.5 micron per line.
Example: 1231,52

The 'dylos.py' script does the following:

1. Reads the data from the serial port 
1. Converts the raw numbers into PM 2.5 values
1. Submits the raw and converted data to InfluxDB

