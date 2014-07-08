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
            self.wii = cwiid.Wiimote('00:23:CC:8F:AA:9E')
            self.wii.enable(cwiid.FLAG_MESG_IFC)
            self.wii.rpt_mode = cwiid.RPT_IR | cwiid.RPT_BTN
            print "Press nExt"
            self.wii2 = cwiid.Wiimote('00:19:1D:60:7E:CE')
            self.wii2.enable(cwiid.FLAG_MESG_IFC)
            self.wii2.rpt_mode = cwiid.RPT_IR | cwiid.RPT_BTN
            print "good"
        except:
            print('Couldnt initialize the wiiMote')

#Average Value Method
    def centerFind(self,rpt):
        xValue=0
        yValue=0
        for i in xrange(len(rpt)):
            xValue+=rpt[i][0]
            yValue+=rpt[i][1]
        xValue= xValue/len(rpt)
        yValue= yValue/len(rpt) 
        return xValue,yValue

    def findDegrees(self, rpt):
        orderList=[]
        cX,cY=self.centerFind(rpt)
        for i in xrange(len(rpt)):
            x,y=rpt[i][0],rpt[i][1]
            theta=self.arctan(cX,cY,x,y)
            theta-=45
            if theta<0:
                theta+=360
            orderList.append([theta,i])
            orderList.sort()
        return orderList

    def arctan(self, cX,cY,c,d):
        #a,b ar1e cx,cy locations
        delX=c-cX
        delY=d-cY
        theta=math.atan2( delX, delY)
        if theta<0:
            theta+=2*math.pi
        return theta*180/math.pi

    def indexData(self,newList):
        tipIndex=newList[1][1]
        tipIndexAngle=newList[1]
        kIndex=newList[0][1]
        kIndexAngle=newList[0][0]
        return tipIndex, tipIndexAngle, kIndex,kIndexAngle

    def thumbData(self,newList):
        tipThumb=newList[2][1]
        tipThumbAngle=newList[2][0]
        kThumb=newList[3][1]
        kThumbAngle=newList[3][0]
        return tipThumb,tipThumbAngle,kThumb,kThumbAngle

    def Dafunc(self,mesg1,mesg2):
        newList=[]  
        for i in xrange(len(mesg1)):
            newList.append([ mesg1[i]['pos'],mesg2[i]["pos"]])
        return newList


    def capture(self):
#Initialization of parameters
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

        while flg==True:            

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

            for event in pygame.event.get():                        
                if event.type==QUIT:
                    flg=False
                    pygame.quit()
                    break
                if event.type==KEYDOWN:
                    if event.key==pygame.K_q: #quits entirely
                        flg=False
                        break


            messages = self.wii2.get_mesg()        
            for mesg in messages:   # Loop through Wiimote Messages
                if mesg[0] == cwiid.MESG_IR: # If message is IR data
        #while recording data
                    if rec_flg == 1:    # If recording
                        cont=-1
                        for s in mesg[1]:   # Loop through IR LED sources
                            cont+=1
                            if s:   # If a source exists
                                t.append(time.time()-t_i)
                                rpt[cont][0]=(1200-s['pos'][0])
                                rpt[cont][1]=s['pos'][1]
            messages = self.wii.get_mesg()        
            for mesg in messages:   # Loop through Wiimote Messages
                if mesg[0] == cwiid.MESG_IR: # If message is IR data
        #while recording data
                    if rec_flg == 1:    # If recording
                        cont=-1
                        for s in mesg[1]:   # Loop through IR LED sources
                            cont+=1
                            if s:   # If a source exists
                                t.append(time.time()-t_i)
                                rpt2[cont][0]=(1200-s['pos'][0])
                                rpt2[cont][1]=s['pos'][1]
            pygame.display.update()      
            print rpt
            print rpt2
            print  "end"

        pygame.quit()
            



"""        

            messages1 = self.wii.get_mesg() 
            print messages1
            messages2 = self.wii2.get_mesg()

            mesg1=messages1[1][1]
            mesg2=messages2[1][1]

            newList=self.Dafunc(mesg1, mesg2)

            for i in xrange(len(newList)):
                rpt[i][0]=1200-newList[i][0][0]
                rpt[i][1]=newList[i][0][1]
                rpt2[i][0]=1200-newList[i][1][0]
                rpt2[i][1]=newList[i][1][1]
                pygame.display.update()  
        pygame.quit()











    #Capturing wii data                    
            messages = self.wii.get_mesg()        
            for mesg in messages:   # Loop through Wiimote Messages
                if mesg[0] == cwiid.MESG_IR: # If message is IR data
        #while recording data
                    if rec_flg == 1:    # If recording
                        cont=-1
                        for s in mesg[1]:   # Loop through IR LED sources
                            cont+=1
                            if s:   # If a source exists
                                t.append(time.time()-t_i)
                                rpt[cont][0]=(1200-s['pos'][0])
                                rpt[cont][1]=s['pos'][1]
                pygame.display.update()     




            messages = self.wii2.get_mesg()        
            for mesg in messages:   # Loop through Wiimote Messages
                if mesg[0] == cwiid.MESG_IR: # If message is IR data
        #while recording data
                    cont=-1
                    for s in mesg[1]:   # Loop through IR LED sources
                        cont+=1
                        if s:   # If a source exists
                            rpt2[cont][0]=(1200-s['pos'][0])
                            rpt2[cont][1]=s['pos'][1]
                pygame.display.update()      







"""