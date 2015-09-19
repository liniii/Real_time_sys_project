# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 14:00:17 2014

@author: ael10hru
"""
import threading

class Monitor(threading.Thread):
    
    def __init__ (self):
        
        threading.Thread.__init__(self)
        self.lock = threading.Lock()  
             
        #refgen Parameters
        self.function = 1 # 1=squarewave -1=position
        self.amplitude = 4
        self.period = 20
        self.sign = -1
        self.ref = 1
        self.U = 0
        self.reg = -1 # -1 = PI+PID, 1 = LQG, 0 = LQR
        self.x1state = 0.0
        
        #controller parameters
        self.Y = [0,0];
        self.offset = 0

	def getOffset(self):
		self.lock.acquire()
		try:
			return self.offset
		finally:
			self.lock.release()

    def getx1State(self): 
        self.lock.acquire()
        try:
            return self.x1state
        finally:
            self.lock.release()
        
    def getU(self):
        self.lock.acquire()
        try:
            return self.U
        finally:
            self.lock.release()
         
    def getReg(self):
        self.lock.acquire()
        try:
            return self.reg
        finally:
            self.lock.release()         
        
    def getAmplitude(self):
        self.lock.acquire()
        try:
            return self.amplitude
        finally:
            self.lock.release()
        
        
    def getPeriod(self):
        self.lock.acquire()
        try:
             return self.period     
        finally:
            self.lock.release()
        
        
    def getFunction(self):
        self.lock.acquire()
        try:
             return self.function       
        finally:
            self.lock.release()
            
    def getRef(self):
        self.lock.acquire()
        try:
             return self.ref       
        finally:
            self.lock.release()   
            
    def getY(self):
        self.lock.acquire()
        try:
             return self.Y       
        finally:
            self.lock.release() 
            
    def getSign(self):
        self.lock.acquire()
        try:
             return self.sign       
        finally:
            self.lock.release()     
                    
      ################################################################## 
    def setx1State(self, x1): 
        self.lock.acquire()
        try:
            self.x1state = x1
        finally:
            self.lock.release()                    
                    
                    
    def setReg(self, regul):
        self.lock.acquire()
        try:
            self.reg = regul
        finally:
            self.lock.release()                     
                    
    def setU(self, u):
        self.lock.acquire()
        try:
            self.U = u 
        finally:
            self.lock.release()

    def setAmplitude(self, amp):
        self.lock.acquire()
        try:
            self.amplitude = amp 
        finally:
            self.lock.release()
        
    def setPeriod(self,per):
        self.lock.acquire()
        try:
            self.period = per
        finally:
            self.lock.release()
            
    def setSign(self,signs):
        self.lock.acquire()
        try:
             self.sign= signs       
        finally:
            self.lock.release()        
        
    def setFunction(self,func):
        self.lock.acquire()
        try:
             self.function = func       
        finally:
            self.lock.release()
            
    def setRef(self,reference):
        self.lock.acquire()
        try:
             self.ref = reference  
        finally:
            self.lock.release()      
            
    def setY(self,y):
        self.lock.acquire()
        try:
             self.Y = y  
        finally:
            self.lock.release()   
        
    
    def setOffset(self, os):
		self.lock.acquire()
		try:
			self.offset = os
		finally:
			self.lock.release()
			
