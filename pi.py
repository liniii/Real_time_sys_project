# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 14:31:36 2014

@author: ael10hru
"""

class pi():
        def __init__(self):
                     
     
            self.K = 2.2
            self.Ti = 0
            self.Tr = 0.5
            self.Beta = 1.0
            self.H = 0.01
            self.I = 0.0
            self.error = 0.0
            self.v = 0.0       
            

        def update_state(self, us):
           try:
                self.I = self.I + (self.K*self.H/self.Ti)*self.error + (self.H/self.Tr)*(us - self.v);
           except ZeroDivisionError:
                self.I = 0

        def calculate_output(self,y0,us):
            self.error = us-y0
            self.v = self.K * (self.Beta * us - y0) + self.I
            return self.v

