########################Table of Contents#######################################
"""
-1. Imports
-2. Threading Class 
-3A. Helper functions to find finger locations
-3B. Helper functions to find if the LEDs are inrange
-4. Helper functions for gestures
-5. Constants and setting up pygame
-6. Starting the threads
-7. Calibration section
-8. Recording section


"""
#-1##############################################################################
import constants as vals
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
#-2##############################################################################

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
                print "Press 1 & 2 on the Wiimote simultaneously to find it"
                self.wii = cwiid.Wiimote()
#                print "yo"
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
                        if rec_flg == 1 or calibration:    # If recording
                            cont=-1
                            for s in mesg[1]:   # Loop through IR LED sources
                                cont+=1
                                if s:   # If a source exists
                                    rpt[cont][0]=(1200-s['pos'][0])
                                    rpt[cont][1]=s['pos'][1]
            except:
#                 print "a aint iterable" #Not necessary
                pass
            self.data=rpt
            queueLock.release()
            sleep(0.001) #really interesting how the sleep makes it work
#-3A############################################################################

def centerFind(rpt):
    xValue=0
    yValue=0
    for i in xrange(len(rpt)):
        xValue+=rpt[i][0]
        yValue+=rpt[i][1]
    xValue= xValue/len(rpt)
    yValue= yValue/len(rpt) 
    return xValue,yValue

def findDegrees(rpt):
    orderList=[]
    cX,cY=centerFind(rpt)
    for i in xrange(len(rpt)):
        x,y=rpt[i][0],rpt[i][1]
        theta=arctan(cX,cY,x,y)
        theta-=45
        if theta<0:
            theta+=360
        orderList.append([theta,i])
        orderList.sort()
    return orderList

def arctan(cX,cY,c,d):
    #a,b ar1e cx,cy locations
    delX=c-cX
    delY=d-cY
    theta=math.atan2( delX, delY)
    if theta<0:
        theta+=2*math.pi
    return theta*180/math.pi

def indexData(newList):
    tipIndex=newList[1][1]
    tipIndexAngle=newList[1]
    kIndex=newList[0][1]
    kIndexAngle=newList[0][0]
    return tipIndex, tipIndexAngle, kIndex,kIndexAngle

def thumbData(newList):
    tipThumb=newList[2][1]
    tipThumbAngle=newList[2][0]
    kThumb=newList[3][1]
    kThumbAngle=newList[3][0]
    return tipThumb,tipThumbAngle,kThumb,kThumbAngle

#-3B############################################################################

def rangeChecker(rptList,LED1, LED2,LED3,LED4):
    sameFlag=0
    #append the new LED position
    LED1.append(rptList[len(rptList)-1][0])
    LED2.append(rptList[len(rptList)-1][1])
    LED3.append(rptList[len(rptList)-1][2])
    LED4.append(rptList[len(rptList)-1][3])
    #check when LED is static
    sameFlag=outOfBounds(LED1,LED2,LED3,LED4)
    return (not (sameFlag)), LED1, LED2,LED3,LED4

#Doesnt Seem to be necessary so commented out
#check when LED is flickering
#        if not(sameFlag):
#            sameFlag=flickering(LED1,LED2,LED3,LED4)

def outOfBounds( LED1,LED2,LED3,LED4):
    sameFlag=0
    if len(LED1)<10 or len(LED2)<10 or len(LED3)<10 or len(LED4)<10:
        pass
    else:
        flg1=checkEqual(LED1)
        flg2=checkEqual(LED2)
        flg3=checkEqual(LED3)
        flg4=checkEqual(LED4)
        if flg1 or flg2 or flg3 or flg4:
            sameFlag=1 #there is one thats same
        listOfLEDs=[LED1,LED2,LED3,LED4]
        for i in xrange(len(listOfLEDs)):
            thisLED=listOfLEDs[i]
            if (not (20<thisLED[len(thisLED)-1][0]<1180)) or (not (20<thisLED[len(thisLED)-1][1]<750)):
                sameFlag=1
                break
    return sameFlag

def checkEqual( ledList):
    flg=0
    if (ledList[(len(ledList)-1)][0]==ledList[(len(ledList)-5)][0] and ledList[(len(ledList)-1)][1]==ledList[(len(ledList)-5)][1]):
        flg=1
    if flg:
        if (ledList[(len(ledList)-1)][0]==ledList[(len(ledList)-9)][0] and ledList[(len(ledList)-1)][1]==ledList[(len(ledList)-9)][1]):
            return flg
        else: 
            flg=0
            return flg
    return flg #its zero

def flickering(LED1,LED2,LED3,LED4):
    flickeringFlag=0
    if len(LED1)<10 or len(LED2)<10 or len(LED3)<10 or len(LED4)<10:
        pass
    else:
        flg1=checkEqual(LED1)
        flg2=checkEqual(LED2)
        flg3=checkEqual(LED3)
        flg4=checkEqual(LED4)
        if flg1 or flg2 or flg3 or flg4:
            flickeringFlag=1 #there is one thats same
    return flickeringFlag

def checkDifference(ledList):
    flg=0
    if ((abs(ledList[(len(ledList)-1)][0]-ledList[(len(ledList)-5)][0])>value) \
        or (abs(ledList[(len(ledList)-1)][1]-ledList[(len(ledList)-5)][1])>value)):
        flg=1
    return flg

#-4#############################################################################

def allAboveGestureRight(rpt,gestureRightThreshHold):
    above=0
    for i in xrange(len(rpt)):
        if rpt[i][0]>=gestureRightThreshHold:
            above+=1
    return above/4
    
def allAboveGestureLeft(rpt,gestureLeftThreshHold):
    above=0
    for i in xrange(len(rpt)):
        if rpt[i][0]<gestureLeftThreshHold:
            above+=1
    return above/4                   

def allAboveGestureUp(rpt,gestureUpThreshHold):
    above=0
    for i in xrange(len(rpt)):
        if rpt[i][1]<gestureUpThreshHold:
            above+=1
    return above/4 

def allAboveGestureDown(rpt,gestureDownThreshHold):
    above=0
    for i in xrange(len(rpt)):
        if rpt[i][1]>=gestureDownThreshHold:
            above+=1
    return above/4        
                  
#-5#############################################################################

#Constants
contDist=0
inrange=0
red = (255,0,0,120)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
yellow = (255,255,0)
gray= (205,200, 177)
rpt=[ [0,0] for i in range(4)]
X=0
Y=0
t=[]
ir_x=[]
ir_y=[]
ir_s=[]
t_i = time.time()  
m = PyMouse()
k = PyKeyboard()
running=False
buff=[[],[]]
maxBuff=20
buff[0]=q.miniQueue(maxBuff)
buff[1]=q.miniQueue(maxBuff)

maxDepthBuff=10
depthBuff=[[],[],[],[]]
depthBuff[0]=q.miniQueue(maxDepthBuff)
depthBuff[1]=q.miniQueue(maxDepthBuff)
depthBuff[2]=q.miniQueue(maxDepthBuff)
depthBuff[3]=q.miniQueue(maxDepthBuff)
##################################################################################################################################################################################################################################################################################################################################
yeah_flg=0
oh_yeah_flg=0






gestures=[[6,2,8,2,8],[9,3,9]]
gestures=[ [str(i2) for i2 in i]for i in gestures]
#recording flags        
rec_flg =0
flg=True
mouse_flg=0
click_flg=0
doubleClick_flg=0
drag_flg=0
dragX=0
dragY=0
wait_flg=0
timeHold=80 #in milliseconds                

#calibration
mouseModeValue=10
clickValue=10
knuckleValue=80
lagValue=100
calibration=False
mouseModeCalib=False
startMouseModeCalib=False
clickingCalib=False
startClickModeCalib=False
mouseModeCalibList=[]
clickingCalibList=[]
rightClickValue=180
#Gesture
gestureRightThreshHold=1000
gestureLeftThreshHold=300
gestureDownThreshHold=720
gestureUpThreshHold=400
gesture_flg_UD=0
gesture_flg_DU=0
gesture_flg_LR=0
gesture_flg_RL=0
#Check inrange
LED1=[]
LED2=[]
LED3=[]
LED4=[]
rptList=[]
#Intialization of GUI
os.environ['SDL_VIDEO_iWINDOW_POS'] = "%d,%d" % (0,0)
pygame.init()
clock=pygame.time.Clock()
myfont=pygame.font.SysFont("monospace",15)
calibFont=pygame.font.SysFont("monospace",20)
depthFont=pygame.font.SysFont("monospace",10)
#the default cursor
DEFAULT_CURSOR = mouse.get_cursor()  
#the hand cursor
_HAND_CURSOR = (
"     XX         ",
"    X..X        ",
"    X..X        ",
"    X..X        ",
"    X..XXXXX    ",
"    X..X..X.XX  ",
" XX X..X..X.X.X ",
"X..XX.........X ",
"X...X.........X ",
" X.....X.X.X..X ",
"  X....X.X.X..X ",
"  X....X.X.X.X  ",
"   X...X.X.X.X  ",
"    X.......X   ",
"     X....X.X   ",
"     XXXXX XX   ")
_HCURS, _HMASK = pygame.cursors.compile(_HAND_CURSOR, ".", "X")
HAND_CURSOR = ((16, 16), (5, 1), _HCURS, _HMASK)

rpt=[ [0,0] for i in range(4)]
rpt2=[ [0,0] for i in range(4)]



infoObject = pygame.display.Info()
width=infoObject.current_w
height=infoObject.current_h
screen=pygame.display.set_mode((width/2,height/2))

#-6#########################################################################################################

wiiMote1 = CountThread(queueLock,"wiiMote1")  #this inits
wiiMote1.start() #run
while wiiMote1.connected==False:
    sleep(1)
    print "waiting for a connection"
wiiMote2 = CountThread(queueLock,"wiiMote2")
wiiMote2.start()
#The display section
timeInitial=time.time()

print('press "c" to calibrate, then')
print('press "r" to start recording')        
while FLG:
#-7#############################################################################
    if calibration: #do calibration
    #Receiving data from the threads
        rpt=wiiMote1.data
        rpt2=wiiMote2.data
        try: #to eliminate the case when theres an error with rpt or rpt2
            rpt[0][0]+0
            rpt2[0][0]+0
        except:
            rpt=[ [0,0] for i in range(4)]
            rpt2=[ [0,0] for i in range(4)]

        newList=findDegrees(rpt) #[(theta1,i1),(theta2,i2)....)]
        tipIndex, tipIndexAngle, kIndex,kIndexAngle=indexData(newList)
        tipThumb,tipThumbAngle,kThumb,kThumbAngle=thumbData(newList)
        averageX,averageY=centerFind(rpt)
#GUI section
        screen.fill(black)
#Drawing the Circles
        pygame.draw.circle(screen, yellow, (rpt[tipIndex][0]/3,rpt[tipIndex][1]/3),10)
        pygame.draw.circle(screen, vals.red, (rpt[kIndex][0]/3,rpt[kIndex][1]/3),10)
        pygame.draw.circle(screen, vals.green, (rpt[tipThumb][0]/3,rpt[tipThumb][1]/3),10)
        pygame.draw.circle(screen, blue, (rpt[kThumb][0]/3,rpt[kThumb][1]/3),10)
        pygame.draw.circle(screen, white, (averageX/3,averageY/3),10)

        mouseModeDistance=fun.distanceVec(\
        [rpt[tipIndex][0]],\
        [rpt[tipIndex][1]],\
        [rpt[tipThumb][0]],\
        [rpt[tipThumb][1]])

        clickingDistance=fun.distanceVec(\
        [rpt[kIndex][0]],\
        [rpt[kIndex][1]],\
        [rpt[tipThumb][0]],\
        [rpt[tipThumb][1]])
#Drawing the instructions
        pygame.draw.rect(screen, gray, (0,5,500,60))

        if not (mouseModeCalib or startClickModeCalib or startMouseModeCalib or clickingCalib):
            Calib1=calibFont.render("Press H to start",1,black)
            screen.blit(Calib1,(0,15))
        if startMouseModeCalib and not mouseModeCalib:
            Calib1=calibFont.render("Tap tip of thumb and tip of index",1,black)
            screen.blit(Calib1,(0,15))
            Calib2=calibFont.render("Press H to complete",1,black)
            screen.blit(Calib2,(0,35))
            pygame.draw.line(screen,white,(rpt[tipThumb][0]/3,rpt[tipThumb][1]/3),(rpt[tipIndex][0]/3,rpt[tipIndex][1]/3),5 )
            mouseModeCalibList.append(mouseModeDistance[0])                
        if startClickModeCalib and not clickingCalib:
            Calib1=calibFont.render("Tap tip of thumb and knuckle of index",1,black)
            screen.blit(Calib1,(0,15))
            Calib2=calibFont.render("Press H to complete",1,black)
            screen.blit(Calib2,(0,35))
            pygame.draw.line(screen,white,(rpt[tipThumb][0]/3,rpt[tipThumb][1]/3),(rpt[kIndex][0]/3,rpt[kIndex][1]/3),5 )
            clickingCalibList.append(clickingDistance[0])                    
        if mouseModeCalib and clickingCalib:
            calibrationDone=1
            Calib1=calibFont.render("Calibration Completed",1,black)
            screen.blit(Calib1,(0,15))
            Calib2=calibFont.render("Press r to start recording",1,black)
            screen.blit(Calib2,(0,35))


#-8#############################################################################
    if rec_flg==1: #Recording
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
        newList=findDegrees(rpt) #returns in from [(theta1,i1),(theta2,i2)....)]
        tipIndex, tipIndexAngle, kIndex,kIndexAngle=indexData(newList)
        tipThumb,tipThumbAngle,kThumb,kThumbAngle=thumbData(newList)
        averageX,averageY=centerFind(rpt) #the center point
    #Find out the location of the 2nd Wiimote LEDs
        newList2=findDegrees(rpt2) #returns in from [(theta1,i1),(theta2,i2)....)]
        tipIndex2, tipIndexAngle2, kIndex2,kIndexAngle2=indexData(newList2)
        tipThumb2,tipThumbAngle2,kThumb2,kThumbAngle2=thumbData(newList2)
    #Check whether LED is in range
        newRpt=copy.deepcopy(rpt)
        rptList.append(newRpt)
        inrange, LED1,LED2,LED3,LED4=rangeChecker(rptList, LED1, LED2,LED3,LED4)


#depth

# Z = f * b/d

#where f is the focal length, b is the baseline, or distance between the cameras, and d the disparity between corresponding points. 
#1cm=37.79527559055 pixels
#35cm=1322.834645669pixels
#6cm= 226.7716535433pixels

#35cm=f*6cm/disparity
#f=35cm/6cm*disparity

        focal=1380 #pixels, I found this online

        disparityTipThumb=fun.distanceVec(\
        [rpt[tipThumb][0]],\
        [rpt[tipThumb][1]],\
        [rpt2[tipThumb2][0]],\
        [rpt2[tipThumb2][1]])[0]

        disparityKThumb=fun.distanceVec(\
        [rpt[kThumb][0]],\
        [rpt[kThumb][1]],\
        [rpt2[kThumb2][0]],\
        [rpt2[kThumb2][1]])[0]

        disparityTipIndex=fun.distanceVec(\
        [rpt[tipIndex][0]],\
        [rpt[tipIndex][1]],\
        [rpt2[tipIndex2][0]],\
        [rpt2[tipIndex2][1]])[0]

        disparityKIndex=fun.distanceVec(\
        [rpt[kIndex][0]],\
        [rpt[kIndex][1]],\
        [rpt2[kIndex2][0]],\
        [rpt2[kIndex2][1]])[0]

        disparityList=[disparityTipThumb,disparityKThumb,disparityTipIndex,disparityKIndex]
        depthList=[]
        for i in xrange(len(disparityList)):    
            if disparityList[i]<1:
                depth=0
            else:
                depth=1.0*focal/disparityList[i]*3.5 #cm, the b value
            depthBuff[i].put(depth)
#            depthList.append(depth)


        screen.fill(black)

        mouseLabel=myfont.render("Mouse:"+" "+str(mouseModeValue) ,1,(255,255,255))
        screen.blit(mouseLabel,(0,80))
        clickLabel=myfont.render("Click:"+" "+str(clickValue) ,1,(255,255,255))
        screen.blit(clickLabel,(0,95))        

        Calib1=calibFont.render("tipThumb:"+str(int(depthBuff[0].mean())),1,white)
        screen.blit(Calib1,(0,115))

        Calib2=calibFont.render("kThumb:"+str(int(depthBuff[1].mean())),1,white)
        screen.blit(Calib2,(0,135))

        Calib3=calibFont.render("tipIndex:"+str(int(depthBuff[2].mean())),1,white)
        screen.blit(Calib3,(0,155))
        
        Calib4=calibFont.render("kIndex:"+str(int(depthBuff[3].mean())),1,white)
        screen.blit(Calib4,(0,175))

        red=(255,0,0)
        tomato=(255,99,71)
        coral=(255,127,80)
        indianRed=(205,92,92)

        green=(0,128,0)
        lime=(0,255,0)
        limeGreen=(50,205,50)
        lightGreen=(144,238,144)

#        pygame.draw.circle(screen, red, (rpt[tipIndex][0]/3,rpt[tipIndex][1]/3),10)
#        pygame.draw.circle(screen, tomato, (rpt[kIndex][0]/3,rpt[kIndex][1]/3),10)
#        pygame.draw.circle(screen, coral, (rpt[tipThumb][0]/3,rpt[tipThumb][1]/3),10)
#        pygame.draw.circle(screen, indianRed, (rpt[kThumb][0]/3,rpt[kThumb][1]/3),10)

        #pygame.draw.circle(screen, green, (rpt2[tipIndex2][0]/3,rpt2[tipIndex2][1]/3),10)
        #pygame.draw.circle(screen, lime, (rpt2[kIndex2][0]/3,rpt2[kIndex2][1]/3),10)
        #pygame.draw.circle(screen, limeGreen, (rpt2[tipThumb2][0]/3,rpt2[tipThumb2][1]/3),10)
        #pygame.draw.circle(screen, lightGreen, (rpt2[kThumb2][0]/3,rpt2[kThumb2][1]/3),10)

        pygame.draw.circle(screen, red, (rpt[tipIndex][0]/3,rpt[tipIndex][1]/3),10)
        pygame.draw.circle(screen, blue, (rpt[kIndex][0]/3,rpt[kIndex][1]/3),10)
        pygame.draw.circle(screen, green, (rpt[tipThumb][0]/3,rpt[tipThumb][1]/3),10)
        pygame.draw.circle(screen, white, (rpt[kThumb][0]/3,rpt[kThumb][1]/3),10)

        pygame.draw.circle(screen, red, (rpt2[tipIndex2][0]/3,rpt2[tipIndex2][1]/3),10)
        pygame.draw.circle(screen, blue, (rpt2[kIndex2][0]/3,rpt2[kIndex2][1]/3),10)
        pygame.draw.circle(screen, green, (rpt2[tipThumb2][0]/3,rpt2[tipThumb2][1]/3),10)
        pygame.draw.circle(screen, white, (rpt2[kThumb2][0]/3,rpt2[kThumb2][1]/3),10)


        #GUI for depth

        pygame.draw.rect(screen, gray, (500,0,1500,1500))
#line(Surface, color, start_pos, end_pos, width=1) -> Rect
        for i in xrange(11):
            offsetY=75
            startPos=(550,offsetY+i*30)
            endPos=(650, offsetY+(i*30))
            pygame.draw.line(screen,black,startPos,endPos)
            depthLabel=depthFont.render( str(5*i),1,black)
            screen.blit(depthLabel,(660,offsetY+i*30))

        pygame.draw.circle(screen, green, (560,int(75+depthBuff[0].mean()*6)),10) #tipThumb
        pygame.draw.circle(screen, white, (580,int(75+depthBuff[1].mean()*6)),10) #kThumb
        pygame.draw.circle(screen, red, (600,int(75+depthBuff[2].mean()*6)),10) #tipindex
        pygame.draw.circle(screen, blue, (620,int(75+depthBuff[3].mean()*6)),10)#kIndex

#Mouse Events
#Drawing the mode
        if mouse_flg:
            MouseKeyboard=myfont.render( "Mouse mode",1,(255,255,255))
        else:
            MouseKeyboard=myfont.render( "Keyboard mode",1,(255,255,255))
        screen.blit(MouseKeyboard,(0,50))
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
#Modifying mouseModeValue with respect to distance between knuckles
        currentKnuckleValue=fun.distanceVec(\
        [rpt[kIndex][0]],\
        [rpt[kIndex][1]],\
        [rpt[kThumb][0]],\
        [rpt[kThumb][1]])[0]

        knuckleRatio=float(currentKnuckleValue/knuckleValue)
        if knuckleRatio>1:
            newMouseModeValue=int(knuckleRatio*mouseModeValue)
            newClickValue=int(knuckleRatio*clickValue)
        else:
            newMouseModeValue=mouseModeValue
            newClickValue=clickValue

#Switching Modes
        
        if 10<=dista[0]<=newMouseModeValue and inrange==1:                
            contDist+=1                        
        if contDist>=timeHold and mouse_flg==0 and drag_flg==0:
            print('Mouse mode activated')
            mouse_flg=1
            contDist=0
            mouse.set_cursor(*HAND_CURSOR)
        if contDist>=timeHold and mouse_flg==1 and drag_flg==0:
            print('Mouse mode deactivated')
            mouse_flg=0
            contDist=0
            mouse.set_cursor(*DEFAULT_CURSOR)
#Adjusting MaxBuff with respect to thumbtip and index knuckle
        if mouse_flg:
            a=40*newClickValue
            maxBuff=a/distClick[0]
            if maxBuff<20:
                maxBuff=20
            elif maxBuff>40:
                maxBuff=40
#Clicking
        if distClick[0]<newClickValue and inrange and mouse_flg and not click_flg:
            click_flg=1
            stime=time.time()
            m.click(buff[0].mean(),buff[1].mean())
            dragX, dragY=buff[0].mean(),buff[1].mean()
            print('Click')
            print distClick[0]
        if (click_flg and (time.time()-stime)*1000>=lagValue and not drag_flg): #so its been 1/2 second, 
            if (distClick[0]>=newClickValue): #if finger is up, then delete flag. Else 
                click_flg=0
                drag_flg=0
                print("reset")
                print distClick[0]
            elif ((dragX-buff[0].mean()>5) or (dragY-buff[1].mean()>5)): #Drag situation
                m.press(dragX,dragY)
                drag_flg=1
                print ("dragging")
                print distClick[0]
        if drag_flg and distClick[0]>=int(1.2*newClickValue): #released the drag
            drag_flg=0
            m.release(buff[0].mean(),buff[1].mean())
            dragX,dragY=0,0
            print("release drag")
            print distClick[0]

##################implement click with finger movement
        if inrange and mouse_flg and not click_flg and not yeah_flg: #raise flg and store current values
            ASDFTTD=depthBuff[0].mean()
            ASDFTKD=depthBuff[1].mean()
            ASDFITD=depthBuff[2].mean()
            ASDFIKD=depthBuff[3].mean()
            yeah_flg=1
            print "yeah"

#         if mouse_flg:        
#             print depthBuff[0].mean(), ASDFTTD

        if inrange and mouse_flg and not click_flg and yeah_flg:
            if depthBuff[0].mean()-ASDFTTD<-3:
                ASDFTTD=depthBuff[0].mean()
                oh_yeah_flg=1
                print "oh yeah"

        if oh_yeah_flg and not click_flg and (depthBuff[0].mean()-ASDFTTD>3):
            click_flg=1
            yeah_flg=0
            oh_yeah_flg=0
            stime=time.time()
            m.click(buff[0].mean(),buff[1].mean())
            dragX, dragY=buff[0].mean(),buff[1].mean()
            print('Click with finger')


#Gestures
#The gesture bounds
        pygame.draw.line(screen,white, (gestureRightThreshHold/3,0),(gestureRightThreshHold/3,800))
        pygame.draw.line(screen,red, (gestureLeftThreshHold/3,0),(gestureLeftThreshHold/3,800))
        pygame.draw.line(screen,blue, (0,gestureDownThreshHold/3),(10000,gestureDownThreshHold/3))
        pygame.draw.line(screen,yellow, (0,gestureUpThreshHold/3),(10000,gestureUpThreshHold/3))
#Swipe Right to Left
        if allAboveGestureRight(rpt,gestureRightThreshHold) and not gesture_flg_RL:
            gestureTime=time.time()
            gesture_flg_RL=1
            print("ready to gesture")
        if gesture_flg_RL and (time.time()-gestureTime)<1:
            if allAboveGestureLeft(rpt, gestureLeftThreshHold):
                k.press_key(k.control_key)
                k.press_key(k.alt_key)
                k.press_key(k.left_key)
                k.release_key(k.control_key)
                k.release_key(k.alt_key)
                k.release_key(k.left_key)
                gesture_flg_RL=0
#Swipe Left to Right
        if allAboveGestureLeft(rpt,gestureLeftThreshHold) and not gesture_flg_LR:
            gestureTime=time.time()
            gesture_flg_LR=1
            print("ready to gesture")
        if gesture_flg_LR and (time.time()-gestureTime)<1:
            if allAboveGestureRight(rpt, gestureRightThreshHold):
                k.press_key(k.control_key)
                k.press_key(k.alt_key)
                k.press_key(k.right_key)
                k.release_key(k.control_key)
                k.release_key(k.alt_key)
                k.release_key(k.right_key)
                gesture_flg_LR=0
#Swipe Down to Up
        if allAboveGestureDown(rpt,gestureDownThreshHold) and not gesture_flg_DU:
            gestureTime=time.time()
            gesture_flg_DU=1
            print("ready to gesture")
        if gesture_flg_DU and (time.time()-gestureTime)<1:
            if allAboveGestureUp(rpt, gestureUpThreshHold):
                k.press_key(k.control_key)
                k.press_key(k.alt_key)
                k.press_key(k.up_key)
                k.release_key(k.control_key)
                k.release_key(k.alt_key)
                k.release_key(k.up_key)
                gesture_flg_DU=0
#Swipe Up to Down
        if allAboveGestureUp(rpt,gestureUpThreshHold) and not gesture_flg_UD:
            gestureTime=time.time()
            gesture_flg_UD=1
            print("ready to gesture")
        if gesture_flg_UD and (time.time()-gestureTime)<1:
            if allAboveGestureDown(rpt, gestureDownThreshHold):
                k.press_key(k.control_key)
                k.press_key(k.alt_key)
                k.press_key(k.down_key)
                k.release_key(k.control_key)
                k.release_key(k.alt_key)
                k.release_key(k.down_key)
                gesture_flg_UD=0
        if gesture_flg_RL and (time.time()-gestureTime)>=1:
            gesture_flg_RL=0
        if gesture_flg_LR and (time.time()-gestureTime)>=1:
            gesture_flg_LR=0
        if gesture_flg_UD and (time.time()-gestureTime)>=1:
            gesture_flg_UD=0
        if gesture_flg_DU and (time.time()-gestureTime)>=1:
            gesture_flg_DU=0



################################################################################################################
        if mouse_flg==1:
            X=rpt[tipIndex][0]
            mouseX=(X-600)*width/400                    
            Y=rpt[tipIndex][1]
            mouseY=(Y-150)*height/290

            """Currently we have the setting such that if there is a single LED that is out of range then
            the mouse wont move. The problem with this is that the range of the mouse gets limited, and 
            some places (such as corners) are difficult/impossible to click. If we eliminate the if statement
            then this problem won't exist, but then it may start to recognize the knuckle LED as the tip and vice 
            versa. So this is a give or take until we have a better filtering method."""

            if inrange:
                buff[0].put(mouseX)
                buff[1].put(mouseY)
                smoothX=np.mean(fun.smooth(buff[0].data, window_len=len(buff[0].data)))
                smoothY=np.mean(fun.smooth(buff[1].data, window_len=len(buff[1].data)))
                
                m.move(buff[0].data[-1],buff[1].data[-1])
#                 m.move(smoothX,smoothY)                    
################################################################################################################


    for event in pygame.event.get():
        if event.type==KEYDOWN:
            if event.key==pygame.K_r: #start recording
                rec_flg=1
                calibration=False
            elif event.key==pygame.K_c: #start calibration
                calibration=1
            elif event.key==pygame.K_s: #pauses the recording
                rec_flg=False
                break
            elif event.key==pygame.K_q: #quits entirely
                FLG=False
                break
            if rec_flg: #if recording, can change the lag time
                if event.key==pygame.K_z:
                    lagValue+=100
                elif event.key==pygame.K_x:
                    lagValue-=100
            #Forced mouse mode
            if event.key==pygame.K_m:
                if mouse_flg==1:
                    mouse_flg=0
                else:
                    mouse_flg=1
                    
        #Mouse events for calibration mode
            if calibration:
                if not mouseModeCalib:
                    if not startMouseModeCalib and event.key==pygame.K_h:
                        startMouseModeCalib=True 
                    elif startMouseModeCalib and event.key==pygame.K_h:
                        mouseModeCalib=True
                        while min(mouseModeCalibList)<50:
                            mouseModeCalibList.remove(min(mouseModeCalibList))
                        mouseModeValue=int(1.2*min(mouseModeCalibList))
                        mouseModeCalib=True
                if mouseModeCalib:
                    if not startClickModeCalib and event.key==pygame.K_h:
                        startClickModeCalib=True
                    elif startClickModeCalib and event.key==pygame.K_h:
                        while min(clickingCalibList)<30:
                            clickingCalibList.remove(min(clickingCalibList))
                        clickValue=int(1.2*min(clickingCalibList))

                        knuckleValue=fun.distanceVec(\
                            [rpt[kIndex][0]],\
                            [rpt[kIndex][1]],\
                            [rpt[kThumb][0]],\
                            [rpt[kThumb][1]])[0]

                        clickingCalib=True                            
        if event.type==QUIT:
            FLG=False
            pygame.quit()
            break
    msElapsed=clock.tick(100)
    pygame.display.update()     
sys.exit()
pygame.quit()


#internal flag to say connected
#aptana

#ask it to run when calling rpt

