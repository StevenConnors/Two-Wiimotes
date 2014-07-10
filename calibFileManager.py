# Calibration File Manager. The file name is defined in the constants.py

import json

class CalibFileManager:
    def __init__(self, fileName = 'calib.data'):
        self.fileName = fileName

    def write(self, mouseModeValue, clickValue):
        calibDic = {}
        calibDic['mouseModeValue'] = mouseModeValue
        calibDic['clickValue'] = clickValue
        #print 'Write Dic: ' + str(calibDic)
        calibJSON = json.dumps(calibDic)
        print 'Write JSON: ' + str(calibJSON)

        calibWriter = open(self.fileName, 'w')
        json.dump(calibJSON, calibWriter)
        calibWriter.close()

    def read(self):
        calibReader = open(self.fileName, 'r')
        calibJSON = json.load(calibReader)
        calibReader.close()
        
        print 'Read JSON: ' + str(calibJSON)
        calibDic = json.JSONDecoder().decode(calibJSON)
        if 'mouseModeValue' in calibDic and 'clickValue' in calibDic:
            rtn = calibDic['mouseModeValue'], calibDic['clickValue']
            print 'Read Value: ' + str(rtn)
        else:
        	print 'Error: invalid key name of calibration data.'
        	rtn = 0, 0
        return rtn

