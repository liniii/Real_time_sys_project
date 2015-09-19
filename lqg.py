# -*- coding: utf-8 -*-
"""
Created on Sat Dec  6 12:22:46 2014

@author: ael10hru
"""
import numpy as np

class lqg():
        def __init__(self,monitor):
                     
                ##discrete ss with added integral action(phie osv)       
                self.A11 = 1.0
                self.A12 = 0.01
                self.A13 = -0.000350357142857
                self.A14 = -0.000000444795302
                self.A21 = 0.0
                self.A22 = 1.0
                self.A23 = -0.070071428571429
                self.A24 = -0.000133438590686
                self.A31 = 0.0
                self.A32 = 0.0
                self.A33 = 1.0
                self.A34 = 0.003808644790230
                self.A41 = 0.0
                self.A42 = 0.0
                self.A43 = 0.0
                self.A44 = 1.0
                self.B1 = -0.000000444795302
                self.B2 = -0.000133438590686
                self.B3 = 0.003808644790230
                self.B4 = 0.0
                self.C11 = 1.0
                self.C12 = 0.0
                self.C13 = 0.0
                self.C14 = 0.0
                self.C21 = 0.0
                self.C22 = 0.0
                self.C23 = 1.0
                self.C24 = 0.0   
                
                self.phie = np.matrix([[self.A11, self.A12, self.A13, self.A14],[self.A21, self.A22, self.A23, self.A24],[self.A31, self.A32, self.A33, self.A34],[self.A41, self.A42, self.A43, self.A44]])
                self.gammae = np.matrix([[self.B1],[self.B2],[self.B3],[self.B4]])
                self.Ce = np.matrix([[self.C11, self.C12, self.C13, self.C14],[self.C21, self.C22, self.C23, self.C24]])
                
                #control parameters
                
                self.L = np.matrix([[-59.173712048800418, -30.341590192858870, 33.775890512758984, 1.0]])
                self.lr = -59.173712048800418
                self.K = np.matrix([[ 0.524493995750967, 0.485155151963079], [0.533378779321671, 0.396416303296761], [ 0.482854817372478, 0.520953777053948],[0.484717931563023, 0.515282018080230]])                          
                
                #initial values
                self.xold = np.matrix([[0.0000],[0.0000],[0.0000],[0.0000]])
                #self.uold = np.matrix([[0.0]])
                #self.yold = np.matrix([[0.0],[0.0]])
                self.mon = monitor


        def update_states(self, u, y):
            #x(k+1) = (phi_e -K*C)*x(k) + gamma_e*u(k) + K*y(k)
                KC = np.dot(self.K , self.Ce)           # KC = K*C
                phieKC = self.phie - KC                 # phieKC = phi_e -K*C
                phieKCx = np.dot(phieKC , self.xold)    # phieKCx =(phi_e -K*C)*x(k)
                gammaeu = np.dot(self.gammae , u)       # self.uold) #gammaeu = gamma_e*u(k)               
                Ky = np.dot(self.K , y)					#self.yold)         # Ky = K*y(k)
                self.xold = phieKCx + gammaeu + Ky
                self.mon.setx1State(self.xold[0,0]/0.055)
            
            
        def calculate_output(self,ref,y):
              u = self.lr*ref -np.dot(self.L, self.xold)
              u_sat = self.Saturation(u[0,0])              
              #self.uold = u_sat
              #self.yold = y
              return u_sat


        def Saturation(self, u):
            sat = 10
            if u>sat:
                return sat
            elif u==-0:
                return 0
            elif u<-sat:
                return -sat
            else:
                return u

                   

              
