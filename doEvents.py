<<<<<<< HEAD

import constants as vals

=======
import doMouse
import doEvents
import doDraw
import doDepth
import doGestures
import constants as vals
import findingPoints
import checkingInRange
import gestureCheck

from pymouse import PyMouse
from pykeyboard import PyKeyboard
>>>>>>> 098035ea117798cf3908cf721c502fcebf4ee6a2
import pygame
from pygame import mouse
from pygame.locals import *
import pickle
<<<<<<< HEAD

import sys


def eventHandling(pygame):
=======
import cwiid, time
from pylab import *
import funcs as fun
import math
import copy
from time import sleep
import sys
import numpy as np
import threading
import os
import miniQueue as q
from calibFileManager import *

global FLG
FLG=1
m = PyMouse()
k = PyKeyboard()

def eventHandling():
>>>>>>> 098035ea117798cf3908cf721c502fcebf4ee6a2
    for event in pygame.event.get():
        if event.type==KEYDOWN:
            if event.key==pygame.K_r: #start recording
                vals.rec_flg=1
                vals.calibration=False
            elif event.key==pygame.K_c: #start vals.calibration
                vals.calibration=1
            elif event.key==pygame.K_s: #pauses the recording
                vals.rec_flg=False
                break
            elif event.key==pygame.K_q: #quits entirely
<<<<<<< HEAD
                print "q pressed"
                vals.quit_FLG=1
=======
                FLG=False
                print "q pressed"
                sys.exit()
                pygame.quit()
                break
            #Load calibration data from file : 'l', load
            elif event.key == pygame.K_l:
                vals.calibLoadFlag = True

>>>>>>> 098035ea117798cf3908cf721c502fcebf4ee6a2
            if vals.rec_flg: #if recording, can change the lag time
                if event.key==pygame.K_z:
                    vals.lagValue+=100
                elif event.key==pygame.K_x:
                    vals.lagValue-=100
            #Forced mouse mode
            if event.key==pygame.K_m:
                if vals.mouse_flg==1:
                    vals.mouse_flg=0
                else:
                    vals.mouse_flg=1
                    
        #Mouse events for vals.calibration mode
            if vals.calibration:
                if not vals.mouseModeCalib:
                    if not vals.startMouseModeCalib and event.key==pygame.K_h:
                        vals.startMouseModeCalib=True 
                    elif vals.startMouseModeCalib and event.key==pygame.K_h:
                        vals.mouseModeCalib=True
                        while min(vals.mouseModeCalibList)<50:
                            vals.mouseModeCalibList.remove(min(vals.mouseModeCalibList))
                        vals.mouseModeValue=int(1.2*min(vals.mouseModeCalibList))
                        vals.mouseModeCalib=True
                if vals.mouseModeCalib:
                    if not vals.startClickModeCalib and event.key==pygame.K_h:
                        vals.startClickModeCalib=True
                    elif vals.startClickModeCalib and event.key==pygame.K_h:
                        while min(vals.clickingCalibList)<30:
                            vals.clickingCalibList.remove(min(vals.clickingCalibList))
                        vals.clickValue=int(1.2*min(vals.clickingCalibList))
<<<<<<< HEAD
                        vals.clickingCalib=True                            
        if event.type==QUIT:
            vals.quit_FLG=1
=======
                        vals.clickingCalib=True  

                        #store them to file.
                        if not vals.calibWriteFinished:
                            calibWriter = CalibFileManager(vals.calibFile)
                            calibWriter.write(vals.mouseModeValue, vals.clickValue)
                            vals.calibWriteFinished = True

            if vals.calibLoadFlag:
                if not vals.calibReadFinished:
                    calibReader = CalibFileManager(vals.calibFile)
                    vals.mouseModeValue = calibReader.read('mouseModeValue')
                    vals.clickValue = calibReader.read('clickValue')
                    vals.clickingCalib = True
                    vals.startClickModeCalib = True
                    vals.mouseModeCalib = True
                    vals.startMouseModeCalib = True
                    
                    vals.calibReadFinished = True
                        
        if event.type==QUIT:
            FLG=False
            pygame.quit()
            break
>>>>>>> 098035ea117798cf3908cf721c502fcebf4ee6a2
