# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 14:06:08 2014

@author: ael10hru
"""

import numpy as np
import threading
import time
import datetime as dt
from pid import pid
from pi import pi
from lqg import lqg
import math as math

class Controller(threading.Thread):
    def __init__(self, monitor, comedi):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.time_sleep = 0
        self.com = comedi
        self.mon = monitor
        self.pid = pid()
        self.pi = pi()
        self.Ts = 0.01
        self.lqg = lqg(self.mon)
        self.meas_time=dt.datetime.now()
        
        self.offset = 0 # offset mittpunkt bom i volt, bom 2 lördag
        self.mon.setOffset(self.offset)
        
    def Saturation(self, u):
        sat = 7
        if u>sat:
            return sat
        elif u==-0:
            return 0
        elif u<-sat:
            return -sat
        else:
            return u
            
    def run(self):
        while self.isAlive():
            self.lock.acquire()
            try:
                #do for both
                time_start = dt.datetime.now()
                self.Y = self.com.getY();
                ref = self.mon.getRef()
                #parametrar för PID, ej skalade    
                self.pos = self.Y[0] - self.offset
                self.vel = self.Y[1]
                self.ang = self.Y[2]
                
                #parametrar för LQG, skalade    
                self.pos_l = self.Y[0]*0.055 - self.offset*0.055
                self.vel_l = self.Y[1]
                self.ang_l = self.Y[2]*4.5 # Vilker i grader
                self.ang_l = self.ang_l*math.pi/180 # Vinkel i radianer
                ref_l = ref*0.055
                
                scaledY = [self.Y[0] - self.offset, self.Y[1], self.Y[2]]                              
                self.mon.setY(scaledY);                 
                
                #pid
                u_pid = self.pid.calculate_output(ref,self.pos)
                us_pid = self.Saturation(u_pid)
                self.pid.update_state(us_pid)
                # pi
                v_pi = self.pi.calculate_output(self.ang,us_pid)
                vs_pi = self.Saturation(v_pi)
                
                if self.mon.getReg() == -1:
                    self.com.putU([vs_pi])
                    self.mon.setU(vs_pi)
                
                self.pi.update_state(vs_pi)                                   
                
                # LQG
                y_lqg = np.matrix([[self.pos_l],[self.ang_l]])
                v_lqg = self.lqg.calculate_output(ref_l, y_lqg)
                
                if self.mon.getReg() == 1:
                    self.mon.setU(v_lqg)
                    self.com.putU([v_lqg])
                    
                self.lqg.update_states(v_lqg, y_lqg)
                
                    
                self.time_sleep = self.Ts - (dt.datetime.now() - time_start).microseconds/1000000.0
                
            finally:
                self.lock.release()
                #self.meas_time = dt.datetime.now()
                #print "Loop time was: {}".format((dt.datetime.now() - self.meas_time).microseconds/1000000.0)
                time.sleep(self.time_sleep if self.time_sleep > 0 else 0)
