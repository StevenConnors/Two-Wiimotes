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



global flg
flg=1

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
                self.wii.enable(cwiid.FLAG_MESG_IFC)
                self.wii.rpt_mode = cwiid.RPT_IR | cwiid.RPT_BTN
                print Label+"connected successfully"
                self.data=[[0,0],[0,0],[0,0],[0,0]]
                done=True
                self.connected=True
            except:
                print('Couldnt initialize the wiiMote')

    def run(self):
        rpt=[ [0,0] for i in range(4)]
        while flg:
            messages = self.wii.get_mesg()  
            try:
                for mesg in messages:   # Loop through Wiimote Messages
                    if mesg[0] == cwiid.MESG_IR: # If message is IR data
        #while recording data
                        if rec_flg == 1 or calibration:    # If recording
                            cont=-1
                            for s in mesg[1]:   # Loop through IR LED sources
                                cont+=1
                                if s:   # If a source exists
                                    rpt[cont][0]=(1200-s['pos'][0])
                                    rpt[cont][1]=s['pos'][1]
            except:
                print "a aint iterable"
            self.data=rpt
            sleep(0.01)
#shouldve placed the getmesg in the thread



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



#Constants

red = (255,0,0,120)
#green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
yellow = (255,255,0)
gray= (205,200, 177)

rpt=[ [0,0] for i in range(4)]
rpt2=[ [0,0] for i in range(4)]

#flg=True
rec_flg=1

os.environ['SDL_VIDEO_iWINDOW_POS'] = "%d,%d" % (0,0)
pygame.init()

myfont=pygame.font.SysFont("monospace",15)
calibFont=pygame.font.SysFont(",monospace",20)

infoObject = pygame.display.Info()
width=infoObject.current_w
height=infoObject.current_h
screen=pygame.display.set_mode((width/2,height/2))
############################################################################################################

for event in pygame.event.get():                        
    if event.type==QUIT:
        pygame.quit()
        break
    if event.type==KEYDOWN:
        if event.key==pygame.K_q: #quits entirely
            pygame.quit()
            break

a = CountThread(queueLock,"a")  #this inits
a.start() #run
while a.connected==False:
    sleep(1)
    print "waiting for a connection"
b = CountThread(queueLock,"b")
b.start()


while flg:
    
    if rec_flg==1:
        rpt=a.data
        rpt2=b.data

        newList=findDegrees(rpt) #[(theta1,i1),(theta2,i2)....)]
        tipIndex, tipIndexAngle, kIndex,kIndexAngle=indexData(newList)
        tipThumb,tipThumbAngle,kThumb,kThumbAngle=thumbData(newList)
        averageX,averageY=centerFind(rpt)

#GUI section
        screen.fill(black)
#Drawing the Circles
        
        red=(255,0,0)
        tomato=(255,99,71)
        coral=(255,127,80)
        indianRed=(205,92,92)

        green=(0,128,0)
        lime=(0,255,0)
        limeGreen=(50,205,50)
        lightGreen=(144,238,144)


        pygame.draw.circle(screen, red, (rpt[tipIndex][0]/3,rpt[tipIndex][1]/3),10)
        pygame.draw.circle(screen, tomato, (rpt[kIndex][0]/3,rpt[kIndex][1]/3),10)
        pygame.draw.circle(screen, coral, (rpt[tipThumb][0]/3,rpt[tipThumb][1]/3),10)
        pygame.draw.circle(screen, indianRed, (rpt[kThumb][0]/3,rpt[kThumb][1]/3),10)

        pygame.draw.circle(screen, green, (rpt2[tipIndex][0]/3,rpt2[tipIndex][1]/3),10)
        pygame.draw.circle(screen, lime, (rpt2[kIndex][0]/3,rpt2[kIndex][1]/3),10)
        pygame.draw.circle(screen, limeGreen, (rpt2[tipThumb][0]/3,rpt2[tipThumb][1]/3),10)
        pygame.draw.circle(screen, lightGreen, (rpt2[kThumb][0]/3,rpt2[kThumb][1]/3),10)

#depth

# Z = f * b/d
        focal=1380 #pixels

        disparityTipThumb=((((rpt[tipThumb][0]-rpt2[tipThumb][0])**2)+(rpt[tipThumb][1]-rpt2[tipThumb][1])**2)**(0.5))
        disparityKThumb=((((rpt[kThumb][0]-rpt2[kThumb][0])**2)+(rpt[kThumb][1]-rpt2[kThumb][1])**2)**(0.5))
        disparityTipIndex=((((rpt[tipIndex][0]-rpt2[tipIndex][0])**2)+(rpt[tipIndex][1]-rpt2[tipIndex][1])**2)**(0.5))
        disparityKIndex=((((rpt[kIndex][0]-rpt2[kIndex][0])**2)+(rpt[kIndex][1]-rpt2[kIndex][1])**2)**(0.5))

        disparityList=[disparityTipThumb,disparityKThumb,disparityTipIndex,disparityKIndex]

        #Calib4=calibFont.render("kIndex:"+str(depthList[3]),1,white)
        #screen.blit(Calib4,(0,75))




        depthList=[]
        for i in xrange(len(disparityList)):    
            if disparityList[i]<1:
                depth="can't find"
            else:
                depth=1.0*focal/disparityList[i]*6 #cm, the b value
            depthList.append(depth)


        #Calib1=calibFont.render("tipThumb:"+str(depthList[0]),1,white)
        #screen.blit(Calib1,(0,15))

        #Calib2=calibFont.render("kThumb:"+str(depthList[1]),1,white)
        #screen.blit(Calib2,(0,35))

        #Calib3=calibFont.render("tipIndex:"+str(depthList[2]),1,white)
        #screen.blit(Calib3,(0,55))
        
        #Calib4=calibFont.render("kIndex:"+str(depthList[3]),1,white)
        #screen.blit(Calib4,(0,75))

    for event in pygame.event.get():                        
        if event.type==QUIT:
            pygame.quit()
            break
        if event.type==KEYDOWN:
            if event.key==pygame.K_q: #quits entirely
                pygame.quit()
                flg=0
                break

    pygame.display.update()     
sys.exit()
pygame.quit()






#internal flag to say connected
#aptana

#ask it to run when calling rpt


# Z = f * b/d

#where f is the focal length, b is the baseline, or distance between the cameras, and d the disparity between corresponding points. 
#1cm=37.79527559055 pixels
#35cm=1322.834645669pixels
#6cm= 226.7716535433pixels

#35cm=f*6cm/disparity
#f=35cm/6cm*disparity