#!/usr/bin/python
import os
import sys
import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


inputfile = sys.argv[1]

def plotter(xaxis, yaxis, xlabel, ylabel, title, filename):


        fig = plt.figure()
        
        ax1 = fig.add_subplot(1,1,1, axisbg='white')

        plt.plot_date(x=xaxis, y=yaxis, fmt="-")


        ax1.xaxis.set_major_locator( mdates.DayLocator() )
        ax1.xaxis.set_major_formatter( mdates.DateFormatter('%Y-%m-%d'))
        ax1.xaxis.set_minor_locator( mdates.HourLocator() )
        ax1.xaxis.set_minor_formatter( mdates.DateFormatter('%H'))


        xax1 = ax1.get_xaxis()
        xax1.set_tick_params(which='major', pad=20)



        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        
        plt.savefig(filename, format='svg')  
        
        

def graph():
	 data = np.loadtxt(inputfile, delimiter=',', unpack=True,
                                       converters = {0: mdates.strpdate2num('%Y-%m-%d %H:%M:%S')}) 
         return data



data = graph()

plotter(data[0],data[1],"time (24h)","Parts x 100 per cubic foot","Particle count below 2.5 micron","pm05.svg")
plotter(data[0],data[2],"time (24h)","Parts x 100 per cubic foot","Particle count above 2.5 micron ","pm25.svg")
