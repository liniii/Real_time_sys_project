# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 14:06:08 2014

@author: ael10hru
"""

class pid():
        def __init__(self):

            
            self.K = -0.17
            self.Ti = 6.4
            self.Td = 1.1
            self.Tr = 0.5
            self.Beta = 1.0
            self.H = 0.01
            self.N = 7
            self.I = 0.0
            self.D = 0.5
            self.yold = 0.0
            self.error = 0.0
            self.v = 0.0
            
            self.ad = self.Td/(self.Td + self.N*self.H)
            self.bd = self.K*self.ad*self.N;
            
        def update_state(self, us):
            
            try:
                if self.I == 0:
                    self.I = self.I + ((self.K*self.H)/self.Ti)*self.error + (self.H/self.Tr)*(us - self.v);
                else:
                    self.I = 0
            except ZeroDivisionError:
                pass


        def calculate_output(self,ref,y):
            self.error = ref-y         
            self.D = self.ad*self.D - self.bd*(y - self.yold);
            self.v = self.K*(self.Beta*ref - y) + self.I + self.D
            self.yold = y;
            
            return self.v


