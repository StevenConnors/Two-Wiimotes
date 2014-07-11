import threading


class CountThread(threading.Thread):   
    connected=False
    def __init__(self, qL,Label):
        threading.Thread.__init__(self)
        self.Label=Label
        done=False
        while not done:
            print "starting"+" "+Label
            try:
                print "Press 1 & 2 on the Wiimote simultaneously, to find it"
                self.wii = cwiid.Wiimote()
                self.wii.enable(cwiid.FLAG_MESG_IFC)
                self.wii.rpt_mode = cwiid.RPT_IR | cwiid.RPT_BTN
                print Label+"connected successfully"
                self.data=0
                done=True
                self.connected=True
            except:
                print('Couldnt initialize the wiiMote')
    
    def run(self):
        rpt=[ [0,0] for i in range(4)]
        while FLG:
            queueLock.acquire()
            messages = self.wii.get_mesg()  
            try:
                for mesg in messages:   # Loop through Wiimote Messages
                    if mesg[0] == cwiid.MESG_IR: # If message is IR data
                        if vals.rec_flg == 1 or vals.calibration:    # If recording
                            cont=-1
                            for s in mesg[1]:   # Loop through IR LED sources
                                cont+=1
                                if s:   # If a source exists
                                    rpt[cont][0]=(1200-s['pos'][0])
                                    rpt[cont][1]=s['pos'][1]
            except:
                pass
            self.data=rpt
            queueLock.release()
            sleep(0.001) #really interesting how the sleep makes it work
