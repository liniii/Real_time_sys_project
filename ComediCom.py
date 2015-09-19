# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 11:29:25 2014

@author: SWAGTON
"""
import comedi
import threading


class ComediCom:

    def __init__(self):
        # Open device
        self.device = comedi.comedi_open('/dev/comedi0')
        # Set max values as numbers
        comedi.comedi_set_global_oor_behavior(comedi.COMEDI_OOR_NUMBER)
        # Get channel range info
        self.range_info_input_1 = comedi.comedi_get_range(self.device, 0 , 0 , 0)
        self.range_info_input_2 = comedi.comedi_get_range(self.device, 0 , 1 , 0)
        self.range_info_output_1 = comedi.comedi_get_range(self.device, 1 , 0 , 0)
        # Get channel max inputs
        self.maxdata_input_1 = comedi.comedi_get_maxdata(self.device,0 ,0)
        self.maxdata_input_2 = comedi.comedi_get_maxdata(self.device,0 ,1)
        self.maxdata_output_1 = comedi.comedi_get_maxdata(self.device,1 ,0)
        self.lock = threading.Lock()       
        
        
    def getY(self):
            self.lock.acquire()        
            # Y1 = Y[0] #angle
            Y1_angle = comedi.comedi_data_read(self.device ,0 ,0 ,0 ,0)
            angle = comedi.comedi_to_phys(Y1_angle[1], self.range_info_input_1, self.maxdata_input_1)
            
            Y2_position = comedi.comedi_data_read(self.device ,0 ,1 ,0 ,0)
            position = comedi.comedi_to_phys(Y2_position[1], self.range_info_input_2, self.maxdata_input_2)
            
            Y = [position, 0.0, angle]
            self.lock.release() 
            
            return Y        
            

    def putU(self, U):
   
            # Convert physical data to raw data
            U1_raw = comedi.comedi_from_phys(U[0],self.range_info_output_1, self.maxdata_output_1)
            # Write the raw data
            comedi.comedi_data_write(self.device , 1 , 0 , 0 , 0 , U1_raw)
            return U1_raw
            
            

            
            
            
            
            
            
            
