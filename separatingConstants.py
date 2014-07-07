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

###############################################################################
queueLock= threading.Lock()
class CountThread(threading.Thread):   
    connected=False
    def __init__(self, qL,Label):
        threading.Thread.__init__(self)
        self.Label=Label
        done=False
        while not done:
            print "starting"+" "+Label
            try:
                print "Press 1 & 2 on the Wiimote simultaneously, to find it"
                self.wii = cwiid.Wiimote()
                self.wii.enable(cwiid.FLAG_MESG_IFC)
                self.wii.rpt_mode = cwiid.RPT_IR | cwiid.RPT_BTN
                print Label+"connected successfully"
                self.data=0
                done=True
                self.connected=True
            except:
                print('Couldnt initialize the wiiMote')
    
    def run(self):
        rpt=[ [0,0] for i in range(4)]
        while FLG:
            queueLock.acquire()
            messages = self.wii.get_mesg()  
            try:
                for mesg in messages:   # Loop through Wiimote Messages
                    if mesg[0] == cwiid.MESG_IR: # If message is IR data
                        if vals.rec_flg == 1 or vals.calibration:    # If recording
                            cont=-1
                            for s in mesg[1]:   # Loop through IR LED sources
                                cont+=1
                                if s:   # If a source exists
                                    rpt[cont][0]=(1200-s['pos'][0])
                                    rpt[cont][1]=s['pos'][1]
            except:
                pass
            self.data=rpt
            queueLock.release()
            sleep(0.001) #really interesting how the sleep makes it work
###############################################################################

#Initialize rpt: (the location of LEDS)
rpt=[ [0,0] for i in range(4)]
rpt2=[ [0,0] for i in range(4)]

#Intialization of Pygame
os.environ['SDL_VIDEO_iWINDOW_POS'] = "%d,%d" % (0,0)
pygame.init()
clock=pygame.time.Clock()
myfont=pygame.font.SysFont("monospace",15)
calibFont=pygame.font.SysFont("monospace",20)
depthFont=pygame.font.SysFont("monospace",10)

infoObject = pygame.display.Info()
width=infoObject.current_w
height=infoObject.current_h
screen=pygame.display.set_mode((width/2,height/2))

#Start the threads ############################################################
wiiMote1 = CountThread(queueLock,"wiiMote1")  #this inits
wiiMote1.start() #run
while wiiMote1.connected==False:
    sleep(1)
    print "waiting for a connection"
wiiMote2 = CountThread(queueLock,"wiiMote2")
wiiMote2.start()
###############################################################################

print('press "c" to calibrate, then')
print('press "r" to start recording')        

while FLG:
    if vals.calibration: #do calibration
    #Receiving data from the threads
        rpt=wiiMote1.data
        rpt2=wiiMote2.data
        try: #to eliminate the case when theres an error with rpt or rpt2
            rpt[0][0]+0
            rpt2[0][0]+0
        except:
            rpt=[ [0,0] for i in range(4)]
            rpt2=[ [0,0] for i in range(4)]
        newList=findingPoints.findDegrees(rpt) #[(theta1,i1),(theta2,i2)....)]
        tipIndex, tipIndexAngle, kIndex,kIndexAngle=findingPoints.indexData(newList)
        tipThumb,tipThumbAngle,kThumb,kThumbAngle=findingPoints.thumbData(newList)
        averageX,averageY=findingPoints.centerFind(rpt)
    #GUI section
        doDraw.drawAllCalibration(screen, rpt, tipIndex, tipThumb,kThumb,kIndex,averageX,averageY)

    if vals.rec_flg==1: #Recording
    #Receiving data from the threads
        rpt=wiiMote1.data
        rpt2=wiiMote2.data
        try: #to eliminate the case when theres an error with rpt or rpt2
            rpt[0][0]+0
            rpt2[0][0]+0
        except:
            rpt=[ [0,0] for i in range(4)]
            rpt2=[ [0,0] for i in range(4)]

    #Finding out the location of the LEDs, tipThumb, kThumb....
        newList=findingPoints.findDegrees(rpt) #returns in from [(theta1,i1),(theta2,i2)....)]
        tipIndex, tipIndexAngle, kIndex,kIndexAngle=findingPoints.indexData(newList)
        tipThumb,tipThumbAngle,kThumb,kThumbAngle=findingPoints.thumbData(newList)
        averageX,averageY=findingPoints.centerFind(rpt) #the center point
    #Find out the location of the 2nd Wiimote LEDs
        newList2=findingPoints.findDegrees(rpt2) #returns in from [(theta1,i1),(theta2,i2)....)]
        tipIndex2, tipIndexAngle2, kIndex2,kIndexAngle2=findingPoints.indexData(newList2)
        tipThumb2,tipThumbAngle2,kThumb2,kThumbAngle2=findingPoints.thumbData(newList2)
    #Check whether LED is in range
        newRpt=copy.deepcopy(rpt)
        vals.rptList.append(newRpt)
        vals.inrange, vals.LED1,vals.LED2,vals.LED3,vals.LED4=checkingInRange.rangeChecker(vals.rptList, vals.LED1, vals.LED2,vals.LED3,vals.LED4)
#Depth
        doDepth.findingDepth(rpt, rpt2, tipThumb,tipThumb2, kThumb,kThumb2, tipIndex,tipIndex2,kIndex,kIndex2)
#GUI
        doDraw.drawAllRecording(screen, rpt, rpt2, tipThumb,tipThumb2, kThumb,kThumb2, tipIndex,tipIndex2,kIndex,kIndex2,averageX,averageY)
#Mouse Events
        doMouse.mouseActivities(rpt, tipIndex,tipThumb,kIndex,kThumb)
#Gestures
        doGestures.gestures(averageX,averageY)

################################################################################################################
        if vals.mouse_flg==1:
            mouseX=(rpt[tipIndex][0]-600)*width/400                    
            mouseY=(rpt[tipIndex][1]-150)*height/290

            """Currently we have the setting such that if there is a single LED that is out of range then
            the mouse wont move. The problem with this is that the range of the mouse gets limited, and 
            some places (such as corners) are difficult/impossible to click. If we eliminate the if statement
            then this problem won't exist, but then it may start to recognize the knuckle LED as the tip and vice 
            versa. So this is a give or take until we have a better filtering method."""

            if vals.inrange:
                vals.buff[0].put(mouseX)
                vals.buff[1].put(mouseY)
                smoothX=np.mean(fun.smooth(vals.buff[0].data, window_len=len(vals.buff[0].data)))
                smoothY=np.mean(fun.smooth(vals.buff[1].data, window_len=len(vals.buff[1].data)))
                m.move(vals.buff[0].data[-1],vals.buff[1].data[-1])
#                 m.move(smoothX,smoothY)                    
################################################################################################################
#Various events (keyborad, quit, etc)
    doEvents.eventHandling(pygame)

    msElapsed=clock.tick(40)
    pygame.display.update()     
sys.exit()
pygame.quit()
