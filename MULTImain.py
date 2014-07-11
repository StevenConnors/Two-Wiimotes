
from time import sleep
import sys, pygame
import numpy as np
import threading
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
import MULTImoteMain


class CountThread(threading.Thread):   
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









pygame.init()

clock = pygame.time.Clock()

size = width, height = 320, 240
screen = pygame.display.set_mode(size)

a = CountThread()
b = CountThread()
a.start()
b.start()


#Constants
speed = [2, 2]
black = 0, 0, 0
red = (255,0,0,120)
X=100
Y=100
X1=200
Y1=200
contDist=0
inrange=0
red = (255,0,0,120)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
yellow = (255,255,0)
rpt=[ [0,0] for i in range(4)]
rpt2=[ [0,0] for i in range(4)]



flg=True
rec_flg=1

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
gestures=[[6,2,8,2,8],[9,3,9]]
gestures=[ [str(i2) for i2 in i]for i in gestures]
#Intialization of GUI
os.environ['SDL_VIDEO_iWINDOW_POS'] = "%d,%d" % (0,0)
pygame.init()

myfont=pygame.font.SysFont("monospace",15)
calibFont=pygame.font.SysFont(",monospace",20)


infoObject = pygame.display.Info()
width=infoObject.current_w
height=infoObject.current_h
screen=pygame.display.set_mode((width/2,height/2))




#The display section
while 1:
	screen.fill(black)
	x,y=a.data
	x1,y1=b.data
	X+=10*x-5
	Y+=10*y-5
	X1+=10*x1-5
	Y1+=10*y1-5
	pygame.draw.circle(screen, red, (X,Y),10)
	pygame.draw.circle(screen, red, (X1,Y1),10)
	msElapsed = clock.tick(30)
	pygame.display.update()


	if rec_flg==1:
        newList=self.findDegrees(rpt) #[(theta1,i1),(theta2,i2)....)]
        tipIndex, tipIndexAngle, kIndex,kIndexAngle=self.indexData(newList)
        tipThumb,tipThumbAngle,kThumb,kThumbAngle=self.thumbData(newList)
        averageX,averageY=self.centerFind(rpt)
#GUI section
        screen.fill(black)
#Drawing the Circles
        pygame.draw.circle(screen, red, (rpt[tipIndex][0]/3,rpt[tipIndex][1]/3),10)
        pygame.draw.circle(screen, red, (rpt[kIndex][0]/3,rpt[kIndex][1]/3),10)
        pygame.draw.circle(screen, red, (rpt[tipThumb][0]/3,rpt[tipThumb][1]/3),10)
        pygame.draw.circle(screen, red, (rpt[kThumb][0]/3,rpt[kThumb][1]/3),10)

        pygame.draw.circle(screen, green, (rpt2[tipIndex][0]/3,rpt2[tipIndex][1]/3),10)
        pygame.draw.circle(screen, green, (rpt2[kIndex][0]/3,rpt2[kIndex][1]/3),10)
        pygame.draw.circle(screen, green, (rpt2[tipThumb][0]/3,rpt2[tipThumb][1]/3),10)
        pygame.draw.circle(screen, green, (rpt2[kThumb][0]/3,rpt2[kThumb][1]/3),10)


        ITLabel=myfont.render(  "IT1"+" "+str((rpt[tipIndex][0]/3,rpt[tipIndex][1]/3)),1,(25,255,255))
        screen.blit(ITLabel,(rpt[tipIndex][0]/3,rpt[tipIndex][1]/3))
        IKLabel=myfont.render(  "IK1"+" "+str((rpt[kIndex][0]/3,rpt[kIndex][1]/3))   ,1,(255,255,255))
        screen.blit(IKLabel,(rpt[kIndex][0]/3,rpt[kIndex][1]/3))
        TTLabel=myfont.render(  "TT1"+" "+str((rpt[tipThumb][0]/3,rpt[tipThumb][1]/3))   ,1,(255,255,255))
        screen.blit(TTLabel,(rpt[tipThumb][0]/3,rpt[tipThumb][1]/3))
        TKLabel=myfont.render(  "TK1"+" "+str((rpt[kThumb][0]/3,rpt[kThumb][1]/3))   ,1,(255,255,255))
        screen.blit(TKLabel,(rpt[kThumb][0]/3,rpt[kThumb][1]/3))

        ITLabel=myfont.render(  "IT2"+" "+str((rpt2[tipIndex][0]/3,rpt2[tipIndex][1]/3)),1,(25,255,255))
        screen.blit(ITLabel,(rpt2[tipIndex][0]/3,rpt2[tipIndex][1]/3))
        IKLabel=myfont.render(  "IK2"+" "+str((rpt2[kIndex][0]/3,rpt2[kIndex][1]/3))   ,1,(255,255,255))
        screen.blit(IKLabel,(rpt2[kIndex][0]/3,rpt2[kIndex][1]/3))
        TTLabel=myfont.render(  "TT2"+" "+str((rpt2[tipThumb][0]/3,rpt2[tipThumb][1]/3))   ,1,(255,255,255))
        screen.blit(TTLabel,(rpt2[tipThumb][0]/3,rpt2[tipThumb][1]/3))
        TKLabel=myfont.render(  "TK2"+" "+str((rpt2[kThumb][0]/3,rpt2[kThumb][1]/3))   ,1,(255,255,255))
        screen.blit(TKLabel,(rpt2[kThumb][0]/3,rpt2[kThumb][1]/3))



    for event in pygame.event.get():                        
        if event.type==QUIT:
            flg=False
            pygame.quit()
            break
        if event.type==KEYDOWN:
            if event.key==pygame.K_q: #quits entirely
                flg=False
                break

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
    pygame.display.update()         
    pygame.quit()