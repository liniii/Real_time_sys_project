# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 14:26:19 2014

@author: elt11legolas
"""
from GUI import GUI
from Monitor import Monitor
from ReferenceGenerator import ReferenceGenerator
from ComediCom import ComediCom
from Controller import Controller

def main():
        
        #Create new threads
        comedi = ComediCom()
        mon = Monitor()
        Gui_Thread = GUI(mon, comedi)
        RefThread = ReferenceGenerator(mon)
        ControlThread = Controller(mon, comedi)

        # set daemon = True to connect all threads exit states such that when one exits, all does
        ControlThread.daemon = True
        RefThread.daemon = True

        # Start new Threads
        ControlThread.start()
        Gui_Thread.start()
        RefThread.start()
        
main()

    
