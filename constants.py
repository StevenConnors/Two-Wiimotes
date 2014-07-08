<<<<<<< HEAD
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


contDist=0
inrange=0

red = (255,0,0,120)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)
yellow = (255,255,0)
gray= (205,200, 177)

buff=[[],[]]
maxBuff=20
buff[0]=q.miniQueue(maxBuff)
buff[1]=q.miniQueue(maxBuff)

#calibration constants
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

#Check inrange
LED1=[]
LED2=[]
LED3=[]
LED4=[]
rptList=[]

#Depth Constants
maxDepthBuff=10
depthBuff=[[],[],[],[]]
depthBuff[0]=q.miniQueue(maxDepthBuff)
depthBuff[1]=q.miniQueue(maxDepthBuff)
depthBuff[2]=q.miniQueue(maxDepthBuff)
depthBuff[3]=q.miniQueue(maxDepthBuff)

#gesture constants
gestureRightThreshHold=1000
gestureLeftThreshHold=450
gestureDownThreshHold=700
gestureUpThreshHold=400

gesture_flg_UD=0
gesture_flg_DU=0
gesture_flg_LR=0
gesture_flg_RL=0

gestureTime=0


#just my constants for enabling actual clicking using thumb
yeah_flg=0
oh_yeah_flg=0
=======
class constants:
    red = (255,0,0,120)
    green = (0,255,0)
>>>>>>> 8bacf8bd14a4cbb62b29c403d308edec70fea01d
