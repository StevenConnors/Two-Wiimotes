# Calibration File Manager. The file name is defined in the constants.py

import json

class CalibFileManager:
    def __init__(self, fileName = 'calib.data'):
        self.fileName = fileName
        self.calibJSON = ''
        self.calibDic = {}

    def write(self, mouseModeValue, clickValue):
        self.calibDic = {}
        self.calibDic['mouseModeValue'] = mouseModeValue
        self.calibDic['clickValue'] = clickValue
        #print 'Write Dic: ' + str(calibDic)
        self.calibJSON = json.dumps(self.calibDic)
        print 'Write JSON: ' + str(self.calibJSON)

        calibWriter = open(self.fileName, 'w')
        json.dump(self.calibJSON, calibWriter)
        calibWriter.close()

    def read(self, keyStr):
        if self.calibJSON == '':
            calibReader = open(self.fileName, 'r')
            self.calibJSON = json.load(calibReader)
            calibReader.close()
            print 'Read JSON: ' + str(self.calibJSON)
            self.calibDic = json.JSONDecoder().decode(self.calibJSON)

        # if 'mouseModeValue' in calibDic and 'clickValue' in calibDic:
        #     rtn = calibDic['mouseModeValue'], calibDic['clickValue']
        #     print 'Read Value: ' + str(rtn)
        if keyStr in self.calibDic:
            rtn = str(self.calibDic[keyStr])
            print 'Read ' + keyStr + ' : ' + rtn
        else:
        	print 'Error: invalid key name of calibration data.'
        	rtn = '0'
        return rtn

