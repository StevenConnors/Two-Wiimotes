from pymouse import PyMouse
from pykeyboard import PyKeyboard
import os
import miniQueue as q
import pygame
from pygame import mouse
from pygame.locals import *
import pickle
import os
import cwiid, time
from numpy import * #Import matrix libraries
from pylab import *
import funcs as fun
import time
import math
import copy
import copy


class mote():
    def __init__(self):
        try:
            print "Press 1 & 2 on the Wiimote simultaneously to find it"
            self.wii = cwiid.Wiimote()
            self.wii.enable(cwiid.FLAG_MESG_IFC)
            self.wii.rpt_mode = cwiid.RPT_IR | cwiid.RPT_BTN
        except:
            print('Couldnt initialize the wiiMote')

    def capture(self):
            messages = self.wii.get_mesg()    
            for mesg in messages:   # Loop through Wiimote Messages
                if mesg[0] == cwiid.MESG_IR: # If message is IR data
        #while recording data
                    if rec_flg == 1 or calibration:    # If recording
                        cont=-1
                        for s in mesg[1]:   # Loop through IR LED sources
                            cont+=1
                            if s:   # If a source exists
                                t.append(time.time()-t_i)
                                rpt[cont][0]=(1200-s['pos'][0])
                                rpt[cont][1]=s['pos'][1]