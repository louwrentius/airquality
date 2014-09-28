airquality
==========

The Dylos DC1100 Pro is an air quality monitor that is capable of
measuring particles between 0.5 and 2.5 micron and between 2.5 and 10 micron.

The measured values as displayed on the device are in parts per 0.01 cubic feet.
This particular model has a serial port that outputs the average values per minute.

The format of this output is <2.5 micron,>2.5 micron per line.
Example: 1231,52

The 'dylos.py' script just captures these values from the serial port and writes
them to a csv file. 

The 'plot.py' script uses this csv file as input to generate graphs in svg format.
The index.html file can be publishes with :

    python -m SimpleHTTPServer 

This will display the index.html and thus the svg files through a webserver.


