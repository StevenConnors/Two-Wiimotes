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


def gestures(averageX,averageY):
#Swipe Right to Left
	if gestureCheck.allAboveGestureRight(averageX,vals.gestureRightThreshHold) and not vals.gesture_flg_RL:
		vals.gestureTime=time.time()
		vals.gesture_flg_RL=1
	if vals.gesture_flg_RL and (time.time()-vals.gestureTime)<1:
		if gestureCheck.allAboveGestureLeft(averageX, vals.gestureLeftThreshHold):
			k.press_key(k.control_key)
			k.press_key(k.alt_key)
			k.press_key(k.left_key)
			k.release_key(k.control_key)
			k.release_key(k.alt_key)
			k.release_key(k.left_key)
			vals.gesture_flg_RL=0
#Swipe Left to Right
	if gestureCheck.allAboveGestureLeft(averageX,vals.gestureLeftThreshHold) and not vals.gesture_flg_LR:
		vals.gestureTime=time.time()
		vals.gesture_flg_LR=1
	if vals.gesture_flg_LR and (time.time()-vals.gestureTime)<1:
		if gestureCheck.allAboveGestureRight(averageX, vals.gestureRightThreshHold):
			k.press_key(k.control_key)
			k.press_key(k.alt_key)
			k.press_key(k.right_key)
			k.release_key(k.control_key)
			k.release_key(k.alt_key)
			k.release_key(k.right_key)
			vals.gesture_flg_LR=0
#Swipe Down to Up
	if gestureCheck.allAboveGestureDown(averageY,vals.gestureDownThreshHold) and not vals.gesture_flg_DU:
		vals.gestureTime=time.time()
		vals.gesture_flg_DU=1
	if vals.gesture_flg_DU and (time.time()-vals.gestureTime)<1:
		if gestureCheck.allAboveGestureUp(averageY, vals.gestureUpThreshHold):
			k.press_key(k.control_key)
			k.press_key(k.alt_key)
			k.press_key(k.up_key)
			k.release_key(k.control_key)
			k.release_key(k.alt_key)
			k.release_key(k.up_key)
			vals.gesture_flg_DU=0
#Swipe Up to Down
	if gestureCheck.allAboveGestureUp(averageY,vals.gestureUpThreshHold) and not vals.gesture_flg_UD:
		vals.gestureTime=time.time()
		vals.gesture_flg_UD=1
	if vals.gesture_flg_UD and (time.time()-vals.gestureTime)<1:
		if gestureCheck.allAboveGestureDown(averageY, vals.gestureDownThreshHold):
			k.press_key(k.control_key)
			k.press_key(k.alt_key)
			k.press_key(k.down_key)
			k.release_key(k.control_key)
			k.release_key(k.alt_key)
			k.release_key(k.down_key)
			vals.gesture_flg_UD=0
			print "went down"
	if vals.gesture_flg_RL and (time.time()-vals.gestureTime)>=1:
		vals.gesture_flg_RL=0
	if vals.gesture_flg_LR and (time.time()-vals.gestureTime)>=1:
		vals.gesture_flg_LR=0
	if vals.gesture_flg_UD and (time.time()-vals.gestureTime)>=1:
		vals.gesture_flg_UD=0
	if vals.gesture_flg_DU and (time.time()-vals.gestureTime)>=1:
		vals.gesture_flg_DU=0