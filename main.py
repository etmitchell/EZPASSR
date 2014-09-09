'''
Created on Jul 7, 2014

@author: EMITCHELL
'''
import csv, tkFileDialog, os
from Tkinter import Tk, Label 
import matplotlib.pyplot as plt
#import numpy as np
import dateutil
from datetime import datetime

def graph_format(plt):
    plt.xlabel('Date',fontsize=12)
    plt.ylabel('Time',fontsize=12)
    
def EZdata(path):
    entertime = []
    datedata = []
    exittime = []
    deltatime = []
    totalmoney = 0
    downtown = 0
    tformat = '%I:%M:%S %p'
    with open(path, 'rb') as csvfile:
        EZline = csv.reader(csvfile, delimiter=",")
        for row in EZline:
            if row[5] not in ('-','Entry Time'): 
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
    print "Total tolls paid over entire EZ-Pass history: " + str(totalmoney)
    print "Total number of trips downtown: " + str(downtown)
    
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
    
window = Tk()
window.title('EZ Pass Data Visualizer')
#window.iconbitmap(os.path.normpath(os.getcwd()) + '\icon.ico')
label = Label()
file_path = tkFileDialog.askopenfilename(title='Select Spreadsheet',initialdir='C:\Users\emitchell\Downloads',multiple=True)
if file_path:
    for f in window.tk.splitlist(file_path):
        f = os.path.normpath(f)
        EZdata(f)
    #label = Label(window,text="Complete.")
else:
    label = Label(window,text="No files selected.")
label.pack()
window.mainloop()