import constants as vals

import pygame

from pygame.locals import *

import funcs as fun


def drawAllRecording(screen, rpt, rpt2, tipThumb,tipThumb2, kThumb,kThumb2, tipIndex,tipIndex2,kIndex,kIndex2,averageX,averageY,myfont, calibFont,depthFont):
    screen.fill(vals.black)

    mouseLabel=myfont.render("Mouse:"+" "+str(vals.mouseModeValue) ,1,(255,255,255))
    screen.blit(mouseLabel,(0,80))
    clickLabel=myfont.render("Click:"+" "+str(vals.clickValue) ,1,(255,255,255))
    screen.blit(clickLabel,(0,95))        

    Calib1=calibFont.render("tipThumb:"+str(int(vals.depthBuff[0].mean())),1,vals.white)
    screen.blit(Calib1,(0,115))

    Calib2=calibFont.render("kThumb:"+str(int(vals.depthBuff[1].mean())),1,vals.white)
    screen.blit(Calib2,(0,135))

    Calib3=calibFont.render("tipIndex:"+str(int(vals.depthBuff[2].mean())),1,vals.white)
    screen.blit(Calib3,(0,155))
    
    Calib4=calibFont.render("kIndex:"+str(int(vals.depthBuff[3].mean())),1,vals.white)
    screen.blit(Calib4,(0,175))

    tipDistance=calibFont.render(str(int(vals.tipDistance)),1,vals.white)
    screen.blit(tipDistance,(0,205))

#main circles
    pygame.draw.circle(screen, vals.red, (rpt[tipIndex][0]/3,rpt[tipIndex][1]/3),10)
    pygame.draw.circle(screen, vals.blue, (rpt[kIndex][0]/3,rpt[kIndex][1]/3),10)
    pygame.draw.circle(screen, vals.green, (rpt[tipThumb][0]/3,rpt[tipThumb][1]/3),10)
    pygame.draw.circle(screen, vals.white, (rpt[kThumb][0]/3,rpt[kThumb][1]/3),10)

    pygame.draw.circle(screen, vals.gray, (averageX/3,averageY/3),13)

    pygame.draw.circle(screen, vals.red, (rpt2[tipIndex2][0]/3,rpt2[tipIndex2][1]/3),10)
    pygame.draw.circle(screen, vals.blue, (rpt2[kIndex2][0]/3,rpt2[kIndex2][1]/3),10)
    pygame.draw.circle(screen, vals.green, (rpt2[tipThumb2][0]/3,rpt2[tipThumb2][1]/3),10)
    pygame.draw.circle(screen, vals.white, (rpt2[kThumb2][0]/3,rpt2[kThumb2][1]/3),10)

#GUI for depth
    pygame.draw.rect(screen, vals.gray, (500,0,1500,1500))
    #Creating the lines
    for i in xrange(11):
        offsetY=75
        startPos=(550,offsetY+i*30)
        endPos=(650, offsetY+(i*30))
        pygame.draw.line(screen,vals.black,startPos,endPos)
        depthLabel=depthFont.render( str(5*i),1,vals.black)
        screen.blit(depthLabel,(660,offsetY+i*30))
    #Depth circles
    pygame.draw.circle(screen, vals.green, (560,int(75+vals.depthBuff[0].mean()*6)),10) #tipThumb
    pygame.draw.circle(screen, vals.white, (580,int(75+vals.depthBuff[1].mean()*6)),10) #kThumb
    pygame.draw.circle(screen, vals.red, (600,int(75+vals.depthBuff[2].mean()*6)),10) #tipindex
    pygame.draw.circle(screen, vals.blue, (620,int(75+vals.depthBuff[3].mean()*6)),10)#kIndex

#The gesture bounds
    pygame.draw.line(screen,vals.white, (vals.gestureRightThreshHold/3,0),(vals.gestureRightThreshHold/3,800))
    pygame.draw.line(screen,vals.red, (vals.gestureLeftThreshHold/3,0),(vals.gestureLeftThreshHold/3,800))
    pygame.draw.line(screen,vals.blue, (0,vals.gestureDownThreshHold/3),(10000,vals.gestureDownThreshHold/3))
    pygame.draw.line(screen,vals.yellow, (0,vals.gestureUpThreshHold/3),(10000,vals.gestureUpThreshHold/3))
#Mouses mode drawing
    if vals.mouse_flg:
        MouseKeyboard=myfont.render( "Mouse mode",1,(255,255,255))
    else:
        MouseKeyboard=myfont.render( "Keyboard mode",1,(255,255,255))
    screen.blit(MouseKeyboard,(0,50))




def drawAllCalibration(screen, rpt, tipIndex, tipThumb,kThumb,kIndex,averageX,averageY,myfont,calibFont,depthFont):
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


    screen.fill(vals.black)
    #Drawing the Circles
    pygame.draw.circle(screen, vals.yellow, (rpt[tipIndex][0]/3,rpt[tipIndex][1]/3),10)
    pygame.draw.circle(screen, vals.red, (rpt[kIndex][0]/3,rpt[kIndex][1]/3),10)
    pygame.draw.circle(screen, vals.green, (rpt[tipThumb][0]/3,rpt[tipThumb][1]/3),10)
    pygame.draw.circle(screen, vals.blue, (rpt[kThumb][0]/3,rpt[kThumb][1]/3),10)
    pygame.draw.circle(screen, vals.white, (averageX/3,averageY/3),10)

    #Drawing the instructions
    pygame.draw.rect(screen, vals.gray, (0,5,500,60))
    if not (vals.mouseModeCalib or vals.startClickModeCalib or vals.startMouseModeCalib or vals.clickingCalib):
        Calib1=calibFont.render("Press H to start",1,vals.black)
        screen.blit(Calib1,(0,15))
    if vals.startMouseModeCalib and not vals.mouseModeCalib:
        Calib1=calibFont.render("Tap tip of thumb and tip of index",1,vals.black)
        screen.blit(Calib1,(0,15))
        Calib2=calibFont.render("Press H to complete",1,vals.black)
        screen.blit(Calib2,(0,35))
        pygame.draw.line(screen,vals.white,(rpt[tipThumb][0]/3,rpt[tipThumb][1]/3),(rpt[tipIndex][0]/3,rpt[tipIndex][1]/3),5 )
        vals.mouseModeCalibList.append(mouseModeDistance[0])                
    if vals.startClickModeCalib and not vals.clickingCalib:
        Calib1=calibFont.render("Tap tip of thumb and knuckle of index",1,vals.black)
        screen.blit(Calib1,(0,15))
        Calib2=calibFont.render("Press H to complete",1,vals.black)
        screen.blit(Calib2,(0,35))
        pygame.draw.line(screen,vals.white,(rpt[tipThumb][0]/3,rpt[tipThumb][1]/3),(rpt[kIndex][0]/3,rpt[kIndex][1]/3),5 )
        vals.clickingCalibList.append(clickingDistance[0])                    
    if vals.mouseModeCalib and vals.clickingCalib:
        calibrationDone=1
        Calib1=calibFont.render("Calibration Completed",1,vals.black)
        screen.blit(Calib1,(0,15))
        Calib2=calibFont.render("Press r to start recording",1,vals.black)
        screen.blit(Calib2,(0,35))


def drawAllMiniRecording(screen, rpt, rpt2, tipThumb,tipThumb2, kThumb,kThumb2, tipIndex,tipIndex2,kIndex,kIndex2,averageX,averageY,myfont, calibFont,depthFont):
    screen.fill(vals.black)

#main circles
    pygame.draw.circle(screen, vals.red, (rpt[tipIndex][0]/10,rpt[tipIndex][1]/10),2)
    pygame.draw.circle(screen, vals.blue, (rpt[kIndex][0]/10,rpt[kIndex][1]/10),2)
    pygame.draw.circle(screen, vals.green, (rpt[tipThumb][0]/10,rpt[tipThumb][1]/10),2)
    pygame.draw.circle(screen, vals.white, (rpt[kThumb][0]/10,rpt[kThumb][1]/10),2)

    pygame.draw.circle(screen, vals.gray, (averageX/10,averageY/10),4)

    pygame.draw.circle(screen, vals.red, (rpt2[tipIndex2][0]/10,rpt2[tipIndex2][1]/10),2)
    pygame.draw.circle(screen, vals.blue, (rpt2[kIndex2][0]/10,rpt2[kIndex2][1]/10),2)
    pygame.draw.circle(screen, vals.green, (rpt2[tipThumb2][0]/10,rpt2[tipThumb2][1]/10),2)
    pygame.draw.circle(screen, vals.white, (rpt2[kThumb2][0]/10,rpt2[kThumb2][1]/10),2)
#The gesture bounds
    pygame.draw.line(screen,vals.white, (vals.gestureRightThreshHold/10,0),(vals.gestureRightThreshHold/10,800))
    pygame.draw.line(screen,vals.red, (vals.gestureLeftThreshHold/10,0),(vals.gestureLeftThreshHold/10,800))
    pygame.draw.line(screen,vals.blue, (0,vals.gestureDownThreshHold/10),(10000,vals.gestureDownThreshHold/10))
    pygame.draw.line(screen,vals.yellow, (0,vals.gestureUpThreshHold/10),(10000,vals.gestureUpThreshHold/10))
#Mouses mode drawing
    if vals.mouse_flg:
        MouseKeyboard=myfont.render("M",1,(255,255,255))
    else:
        MouseKeyboard=myfont.render( "K",1,(255,255,255))
    screen.blit(MouseKeyboard,(0,0))



def drawAllMiniCalibration(screen, rpt, tipIndex, tipThumb,kThumb,kIndex,averageX,averageY,myfont,calibFont,depthFont):
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

    screen.fill(vals.black)
    #Drawing the Circles
    pygame.draw.circle(screen, vals.yellow, (rpt[tipIndex][0]/10,rpt[tipIndex][1]/10),2)
    pygame.draw.circle(screen, vals.red, (rpt[kIndex][0]/10,rpt[kIndex][1]/10),2)
    pygame.draw.circle(screen, vals.green, (rpt[tipThumb][0]/10,rpt[tipThumb][1]/10),2)
    pygame.draw.circle(screen, vals.blue, (rpt[kThumb][0]/10,rpt[kThumb][1]/10),2)
    pygame.draw.circle(screen, vals.white, (averageX/10,averageY/10),3)

    if not (vals.mouseModeCalib or vals.startClickModeCalib or vals.startMouseModeCalib or vals.clickingCalib):
        print "Press H to start"
    if vals.startMouseModeCalib and not vals.mouseModeCalib:
        print "Tap tip of thumb and tip of index"
        print "Press H to complete"
        pygame.draw.line(screen,vals.white,(rpt[tipThumb][0]/10,rpt[tipThumb][1]/10),(rpt[tipIndex][0]/10,rpt[tipIndex][1]/10),2 )
        vals.mouseModeCalibList.append(mouseModeDistance[0])                
    if vals.startClickModeCalib and not vals.clickingCalib:
        print "Tap tip of thumb and knuckle of index"
        print "Press H to complete"
        pygame.draw.line(screen,vals.white,(rpt[tipThumb][0]/10,rpt[tipThumb][1]/10),(rpt[kIndex][0]/10,rpt[kIndex][1]/10),2 )
        vals.clickingCalibList.append(clickingDistance[0])                    
    if vals.mouseModeCalib and vals.clickingCalib:
        print "Calibration Completed"
        print "Press r to start recording"
        calibrationDone=1