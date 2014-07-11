import findingPoints


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