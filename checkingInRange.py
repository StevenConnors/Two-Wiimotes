

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