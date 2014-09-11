"""
Author: dasbutter
EZPass operates in 15 U.S. States with 26 million transponders in use by 25 agencies.
This is a simple way to import and view EZPASS data lifted off of your EZPASS account.
Note: EZPass only keeps entry time on file for 12 months. We ignore any timeframes
without entry time.
Currently only accounts for US Rt 90 in the Greater Boston Area.

EZPASS is Property of its respective owners.

TODO: Add functionality to login, pull, and format data so it's seamless.
      Integrate into a Django webapp.
"""
import csv, tkFileDialog, os
from os.path import expanduser
from Tkinter import Tk, Label 
import matplotlib.pyplot as plt
#import numpy as np
import dateutil
from datetime import datetime

def graph_format(plt):
    plt.xlabel('Date',fontsize=12)
    plt.ylabel('Time',fontsize=12)
    
def EZdata(path):
    entertime, datedata, exittime, deltatime, deltamins = ([] for i in range(5))    
    totalmoney = downtown = avgdelta = total = maximum = minimum = 0
    global etime,dates,exitt,delta
    tformat = '%I:%M:%S %p'
    with open(path, 'rb') as csvfile:
        EZline = csv.reader(csvfile, delimiter=",")
        for row in EZline:
            if row[5] not in ('-','Entry Time','','-0'): 
                entertime.append(row[5])
                datedata.append(row[0])
                exittime.append(row[8])
                deltatime.append(str(datetime.strptime(row[8],tformat) - datetime.strptime(row[5],tformat)))
            if row[4] not in ('-','Activity','PYMT'):
                totalmoney += float(str(row[11]).strip('$'))
            if row[9] in ('18','19','20','26'):
                downtown += 1
    etime = [dateutil.parser.parse(s) for s in entertime]
    dates = [dateutil.parser.parse(s) for s in datedata]
    exitt = [dateutil.parser.parse(s) for s in exittime]
    delta = [dateutil.parser.parse(s) for s in deltatime]
    
    for i in delta:
        total += i.minute
        deltamins.append(i.minute)
        if i.minute > maximum:
            maximum = i.minute
        if i.minute < minimum and i.minute != 0:
            minimum = i.minute
    avgdelta = (sum(deltamins)/len(deltamins))
    
    print "Total tolls paid over entire EZ-Pass history: $%s" %totalmoney
    print "Total number of trips to downtown Boston: %s" %downtown
    print "Average time on tolled roads: %s minutes" %avgdelta
    print "Total time spend on tolled roads: %s minutes." %total + " ("+ str((total/60)) + ") hours."
    print "Max time on tolled road was %s minutes." %maximum
    print "Min time on tolled road was %s minutes." %minimum
    
    plot()

def plot():
    #Plot the data on two graphs: time in and time out on left,
    #time delta on right.
    plt.subplot(1,2,1)
    plt.plot(dates,etime,'ro')
    plt.hold(True)
    plt.plot(dates,exitt,'bo')
    graph_format(plt)
    plt.hold(True)
    plt.title(r'EZ Pass In/Out',fontsize=20)
    plt.subplot(1,2,2)
    plt.plot(dates,delta,'go')
    graph_format(plt)
    plt.title('Time Delta',fontsize=20)
    plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
    plt.show()

def main():    
    window = Tk()
    window.title('EZ Pass Data Visualizer')
    #window.iconbitmap(os.path.normpath(os.getcwd()) + '\icon.ico')
    label = Label()
    file_path = tkFileDialog.askopenfilename(title='Select Spreadsheet',initialdir=expanduser("~\Downloads"),multiple=False)
    if file_path:
        for f in window.tk.splitlist(file_path):
            f = os.path.normpath(f)
            EZdata(f)
        else:
            label = Label(window,text="No files selected.")
        label.pack()
        window.mainloop()

main()