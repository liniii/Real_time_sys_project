# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 15:08:14 2014

@author: ael10hru

"""
import time
from GUI import GUI
from Monitor import Monitor
from ReferenceGenerator import ReferenceGenerator
from ComediCom import ComediCom

    
def main():
        
        # Create new threads
        com = ComediCom()
        u = 0
        com.putU([u])
        
            
            #print Y[0]
#        mon = Monitor()
#        Gui_Thread = GUI(mon)
#        ControllThread = Controller(mon)
#        RefThread = ReferenceGenerator(mon)
#        RefThread.daemon = True
#        ControllThread.daemon = True
#        # Start new Threads
#        Gui_Thread.start()
#        ControllThread.start()
#        RefThread.start()
#        for x in range(0, 5):
#            y = com.getY()
#            print y
#            time.sleep(2)
        
"""if __name__ == '__main__':"""
main()

    
