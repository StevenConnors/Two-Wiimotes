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
import pygame
from pygame import mouse
from pygame.locals import *
import pickle
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

global FLG
FLG=1
m = PyMouse()
k = PyKeyboard()



def mouseActivities(rpt, tipIndex,tipThumb,kIndex,kThumb):
#Distance for switching modes
    dista=fun.distanceVec(\
    [rpt[tipIndex][0]],\
    [rpt[tipIndex][1]],\
    [rpt[tipThumb][0]],\
    [rpt[tipThumb][1]])
#Distance for clicking - thumb tip to index knuckle
    distClick=fun.distanceVec(\
    [rpt[kIndex][0]],\
    [rpt[kIndex][1]],\
    [rpt[tipThumb][0]],\
    [rpt[tipThumb][1]])
#Modifying vals.mouseModeValue with respect to distance between knuckles
    currentKnuckleValue=fun.distanceVec(\
    [rpt[kIndex][0]],\
    [rpt[kIndex][1]],\
    [rpt[kThumb][0]],\
    [rpt[kThumb][1]])[0]

    knuckleRatio=float(currentKnuckleValue/vals.knuckleValue)
    if knuckleRatio>1:
        newMouseModeValue=int(knuckleRatio*vals.mouseModeValue)
        newClickValue=int(knuckleRatio*vals.clickValue)
    else:
        newMouseModeValue=vals.mouseModeValue
        newClickValue=vals.clickValue

#Switching Modes
    
    if 10<=dista[0]<=newMouseModeValue and vals.inrange==1:                
        vals.contDist+=1                        
    if vals.contDist>=vals.timeHold and vals.mouse_flg==0 and vals.drag_flg==0:
        print('Mouse mode activated')
        vals.mouse_flg=1
        vals.contDist=0
    if vals.contDist>=vals.timeHold and vals.mouse_flg==1 and vals.drag_flg==0:
        print('Mouse mode deactivated')
        vals.mouse_flg=0
        vals.contDist=0
#Adjusting MaxBuff with respect to thumbtip and index knuckle
    if vals.mouse_flg:
        a=40*newClickValue
        vals.maxBuff=a/distClick[0]
        if vals.maxBuff<20:
            vals.maxBuff=20
        elif vals.maxBuff>40:
            vals.maxBuff=40
#Clicking
    if distClick[0]<newClickValue and vals.inrange and vals.mouse_flg and not vals.click_flg:
        vals.click_flg=1
        stime=time.time()
        m.click(vals.buff[0].mean(),vals.buff[1].mean())
        vals.dragX, vals.dragY=vals.buff[0].mean(),vals.buff[1].mean()
        print('Click')
        print distClick[0]
    if (vals.click_flg and (time.time()-stime)*1000>=vals.lagValue and not vals.drag_flg): #so its been 1/2 second, 
        if (distClick[0]>=newClickValue): #if finger is up, then delete flag. Else 
            vals.click_flg=0
            vals.drag_flg=0
            print("reset")
            print distClick[0]
        elif ((vals.dragX-vals.buff[0].mean()>5) or (vals.dragY-vals.buff[1].mean()>5)): #Drag situation
            m.press(vals.dragX,vals.dragY)
            vals.drag_flg=1
            print ("dragging")
            print distClick[0]
    if vals.drag_flg and distClick[0]>=int(1.2*newClickValue): #released the drag
        vals.drag_flg=0
        m.release(vals.buff[0].mean(),vals.buff[1].mean())
        vals.dragX,vals.dragY=0,0
        print("release drag")
        print distClick[0]

##################implement click with finger movement Still testing#################################
    if vals.inrange and vals.mouse_flg and not vals.click_flg and not vals.yeah_flg: #raise flg and store current values
        ASDFTTD=vals.depthBuff[0].mean()
        ASDFTKD=vals.depthBuff[1].mean()
        ASDFITD=vals.depthBuff[2].mean()
        ASDFIKD=vals.depthBuff[3].mean()
        vals.yeah_flg=1
        print "yeah"

#         if vals.mouse_flg:        
#             print vals.depthBuff[0].mean(), ASDFTTD

    if vals.inrange and vals.mouse_flg and not vals.click_flg and vals.yeah_flg:
        if vals.depthBuff[0].mean()-ASDFTTD<-3:
            ASDFTTD=vals.depthBuff[0].mean()
            print "oh yeah"

    if vals.oh_yeah_flg and not vals.click_flg and (vals.depthBuff[0].mean()-ASDFTTD>3):
        vals.click_flg=1
        vals.yeah_flg=0
        vals.oh_yeah_flg=0
        stime=time.time()
        m.click(vals.buff[0].mean(),vals.buff[1].mean())
        vals.dragX, vals.dragY=vals.buff[0].mean(),vals.buff[1].mean()
        print('Click with finger')
