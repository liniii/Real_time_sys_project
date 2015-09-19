# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 13:05:15 2014

@author: ael10hru
"""
import threading
import time
import numpy as np
import pylab
import Tkinter
import matplotlib.font_manager as font_manager
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GUI(threading.Thread):
    
    def __init__ (self,monitor, comedi):
        #initiates the GUI class
        threading.Thread.__init__(self)
        self.mon = monitor
        self.times=[]
        self.times = [0 for x in range(100)]
        self.flag = 0
        self.lock = threading.Lock()
        self.com  = comedi
        
    def GetAndAppend(self):
        #adds new data to the vectors to be plotted
        if self.flag == 0:
            self.start = time.time()
            self.flag = 1
        self.lock.acquire()
        try:
            if len(self.refValues)>99:
                self.refValues.pop(0)
                self.uValues.pop(0)
                self.times.pop(0)
            self.refValues.append(self.mon.getRef())    # the reference value
            self.realValues.append(self.mon.getY()[0])  # Y[0] is the position of the ball
            self.times.append(time.time()-self.start)
            self.uValues.append(self.mon.getU())        # the control signal 
            self.x1state.append(self.mon.getx1State())  # the estimated position of the ball
            self.root.after(25,GUI.GetAndAppend,self)
        finally:
            self.lock.release()


    def RealtimePloter(self):
        #plots the new data         
        self.lock.acquire()
        try:
           NumberSamples=len(self.refValues)
           CurrentXAxis = np.linspace(min(self.times),max(self.times),100)
           self.line1[0].set_data(CurrentXAxis,pylab.array(self.refValues[-NumberSamples:]))
           self.line2[0].set_data(CurrentXAxis,pylab.array(self.realValues[-NumberSamples:]))
           self.line3[0].set_data(CurrentXAxis,pylab.array(self.uValues[-NumberSamples:]))
           self.line4[0].set_data(CurrentXAxis,pylab.array(self.x1state[-NumberSamples:]))
           self.ax.axis([CurrentXAxis.min(),CurrentXAxis.max(),-10,10])
           self.canvas.draw()
           self.root.after(25,GUI.RealtimePloter,self)
           
        finally:
            self.lock.release()

    def _quit(self):
            #shuts down the program            
            self.lock.acquire()
            try:
                self.mon.setRef(0)
                self.com.putU([0.0])                
                self.root.quit()     # stops mainloop    
                self.root.destroy()  # this is necessary on Windows to prevent
                   
            finally:
                self.com.putU([0.0])
                self.lock.release()        
        
    def setAmplitude(self):
        #sets new amplitude from scale
        self.mon.setAmplitude(self.amplitudeScale.get())
              
    def setPeriod(self):
        #sets new period from scale
        self.mon.setPeriod(self.periodScale.get()) 
        
    def changeRegulLQG(self):
        #changes to LQG
        self.mon.setReg(1)
        self.LQGButton.configure(bg = 'red')
        self.PIPIDButton.configure(bg = 'grey')
            
    def changeRegulPIPID(self):
        #changes to PI+PID
        self.mon.setReg(-1)
        self.PIPIDButton.configure(bg = 'red')
        self.LQGButton.configure(bg = 'grey')

    def changeFunction(self):
        # changes reference function
        if self.mon.getFunction()==1:
            self.functionButton['text'] = 'Position ref'
        else:
            self.functionButton['text'] = 'Square-wave'
        self.mon.setFunction(-1*self.mon.getFunction())

        
    def run(self):
        
            #creates main window and plot
            self.root = Tkinter.Tk()
            self.root.wm_title("Realtime plot")
            self.xAchse=pylab.arange(0,100,1)
            self.yAchse=pylab.array([0]*100)
            self.fig = pylab.figure(1)
            self.ax = self.fig.add_subplot(111)
            self.ax.grid(True)
            self.ax.set_title("")
            self.ax.set_xlabel("Time")
            self.ax.set_ylabel("Amplitude")
            self.ax.axis([0,100,-10,10])
            self.line1 = self.ax.plot(self.xAchse,self.yAchse,'r-', label='$ Reference$')
            self.line2 = self.ax.plot(self.xAchse,self.yAchse,'b-', label='$ Position$')
            self.line3 = self.ax.plot(self.xAchse,self.yAchse,'g-', label='$ Control signal$')
            self.line4 = self.ax.plot(self.xAchse,self.yAchse,'m-', label='$ Estimated position$')
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
            self.canvas.show()
            self.canvas.get_tk_widget().pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)
            self.canvas._tkcanvas.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)
            font_prop = font_manager.FontProperties(size=10)
            self.ax.legend(loc='lower right', prop=font_prop, numpoints=1)
            #initiate  vectors to be ploted            
            self.refValues=[]
            self.refValues = [0 for x in range(100)]
            
            self.realValues=[]
            self.realValues = [0 for x in range(100)] 
            
            self.uValues=[]
            self.uValues = [0 for x in range(100)]    
            
            self.x1state=[]
            self.x1state = [0 for x in range(100)] 
            
            #quit button
            self.quitButton = Tkinter.Button(master=self.root, text='Quit', command=lambda: GUI._quit(self))
            self.quitButton.pack(side=Tkinter.RIGHT)
            
            #regulator buttons
            self.LQGButton = Tkinter.Button(master=self.root, text='LQG', bg='grey', command=lambda: GUI.changeRegulLQG(self))
            self.LQGButton.pack(side=Tkinter.RIGHT)
            
            self.PIPIDButton = Tkinter.Button(master=self.root, text='PI PID', bg = 'red', command=lambda: GUI.changeRegulPIPID(self))
            self.PIPIDButton.pack(side=Tkinter.RIGHT)
            
                        
            # reference function button            
            self.functionButton = Tkinter.Button(master=self.root, text='Square-wave', command=lambda: GUI.changeFunction(self))
            self.functionButton.pack(side=Tkinter.LEFT)
            
            
            #amplitude stuff
            self.amplitudeScale = Tkinter.Scale(master=self.root,label="Amplitude:", from_=0, to=9,sliderlength=10,length=self.ax.patch.get_window_extent().width, orient=Tkinter.HORIZONTAL)
            self.amplitudeScale.set(self.mon.getAmplitude())            
            self.ampButton = Tkinter.Button(master=self.root, text='Set Amplitude', command=lambda: GUI.setAmplitude(self))
            self.ampButton.pack(side=Tkinter.BOTTOM) 
            self.amplitudeScale.pack(side=Tkinter.BOTTOM)
            
            #period stuff
            self.periodScale = Tkinter.Scale(master=self.root,label="Period in seconds", from_=1, to=20,sliderlength=20,length=self.ax.patch.get_window_extent().width, orient=Tkinter.HORIZONTAL)
            self.periodScale.set(10)
            self.periodButton = Tkinter.Button(master=self.root, text='Set Period', command=lambda: GUI.setPeriod(self))
            self.periodButton.pack(side=Tkinter.BOTTOM)
            self.periodScale.pack(side=Tkinter.BOTTOM)
            
            # do stuff
            self.root.protocol("WM_DELETE_WINDOW", GUI._quit)  #thanks aurelienvlg
            self.root.after(25,GUI.GetAndAppend(self))
            self.root.after(25,GUI.RealtimePloter(self))
            Tkinter.mainloop()
            
