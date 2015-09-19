# -*- coding: utf-8 -*-
"""
Hanna är bäst!


"""
import threading
import time

class ReferenceGenerator(threading.Thread):
    
    

    def __init__ (self,monitor):
        threading.Thread.__init__(self)
        self.mon = monitor
                                      
    def run(self):
                
        while self.isAlive():
            if self.mon.getFunction() == 1:
                    self.mon.setSign(-1*self.mon.getSign()) 
                    self.mon.setRef(self.mon.getAmplitude()*self.mon.getSign())         
        
            elif self.mon.getFunction() == -1:
                    self.mon.setRef(self.mon.getAmplitude())
                        
            time.sleep(self.mon.getPeriod()/2)
