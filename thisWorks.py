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
            sleep(0.001)
#shouldve placed the getmesg in the thread


#Constants

red = (255,0,0,120)
green = (0,255,0)
black=(0,0,0)

rpt=[ [0,0] for i in range(4)]
rpt2=[ [0,0] for i in range(4)]

#flg=True
rec_flg=1

os.environ['SDL_VIDEO_iWINDOW_POS'] = "%d,%d" % (0,0)
pygame.init()

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
#The display section
print 'not yet'
timeInitial=time.time()
while flg:
    print 'in'
    
    if rec_flg==1:
        print "1st"+str(time.time()-timeInitial)
        rpt=a.data
        rpt2=b.data
        print "2nd"+str(time.time()-timeInitial)

        
        tipIndex=0
        kIndex=1
        tipThumb=2
        kThumb=3

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
#aptanath