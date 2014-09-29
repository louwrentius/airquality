#!/usr/bin/python
# coding: utf-8
#
# This code is horrible. 
#
import os
import sys
import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties


inputfile = sys.argv[1]

def cubicmeters(array,factor):

    temp = [x*3551.5*factor for x in array]
    
    return temp


def plotter(xaxis, yaxis, xlabel, ylabel, title, filename, factor, limit1, limit2, convert):


        if convert:
            yaxis = cubicmeters(yaxis, factor)   

        fig = plt.figure(figsize=(10,8))
        
        ax1 = fig.add_subplot(1,1,1, axisbg='white')

        plt.plot_date(x=xaxis, y=yaxis, fmt="-", label="Measurement")

        if convert:
            plt.axhline(y=limit1, linewidth=1,color='r',label="WHO AQG Limit")
            plt.axhline(y=limit2, linewidth=1,color='c',label="European Limit 2015")


        ax1.xaxis.set_major_locator( mdates.DayLocator() )
        ax1.xaxis.set_major_formatter( mdates.DateFormatter('%Y-%m-%d'))
        ax1.xaxis.set_minor_locator( mdates.HourLocator() )
        ax1.xaxis.set_minor_formatter( mdates.DateFormatter('%H'))


        xax1 = ax1.get_xaxis()
        xax1.set_tick_params(which='major', pad=20)
        
        ax1.set_ylim(0,)
    
        fontP = FontProperties()
        fontP.set_size('small')

        if convert:
            ax1.legend(loc='lower center', fancybox=True, shadow=True, ncol=3, bbox_to_anchor=(0.5, -0.2), prop = fontP)

        ax1.set_position([0.1,0.2,0.6,0.7])
        
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        
        plt.savefig(filename, format='png')  
        
        
    


def graph():
	 data = np.loadtxt(inputfile, delimiter=',', unpack=True,
                                       converters = {0: mdates.strpdate2num('%Y-%m-%d %H:%M:%S')}) 

         return data



data = graph()

plotter(data[0],data[1],"time (24h)",u"Particles x 100 per cubic foot","PM2.5 Measurement","pm05.png",0.000000589,10,25,False)
plotter(data[0],data[1],"time (24h)",u"µg per m$^3$ (aproximation)","PM2.5 Measurement","pm05-PM.png",0.000000589,10,25,True)
plotter(data[0],data[2],"time (24h)",u"Particles x 100 per cubic foot","PM10 Measurement","pm25.png",0.000121,20,40,False)
plotter(data[0],data[2],"time (24h)",u"µg per m$^3$ (aproximation)","PM10 Measurement","pm25-PM.png",0.000121,20,40,True)
