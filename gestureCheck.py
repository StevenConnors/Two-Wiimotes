

def allAboveGestureRight(averageX,gestureRightThreshHold):
    return averageX>=gestureRightThreshHold
    
def allAboveGestureLeft(averageX,gestureLeftThreshHold):
    return averageX<=gestureLeftThreshHold

def allAboveGestureUp(averageY,gestureUpThreshHold):
    return averageY<=gestureUpThreshHold
    
def allAboveGestureDown(averageY,gestureDownThreshHold):
    return averageY>=gestureDownThreshHold
                  