import miniQueue as q



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

#
rpt=[ [0,0] for i in range(4)]
rpt2=[ [0,0] for i in range(4)]

tipThumb=0
tipIndex=0
kThumb=0
kIndex=0

tipThumb2=0
tipIndex2=0
kThumb2=0
kIndex2=0

tipIndexAngle=0
kIndexAngle=0
tipThumbAngle=0
kThumbAngle=0





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

#calibration file using JSON
calibFile = 'calib.data'
calibLoadFlag = False
calibReadFinished = False
calibWriteFinished = False

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
stime=0

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

ASDFTTD=0
ASDFTKD=0
ASDFITD=0
ASDFIKD=0