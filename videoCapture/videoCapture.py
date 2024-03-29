#!/usr/bin/env python3
# import the opencv library
import cv2
import time
import RPi.GPIO as GPIO

'''
arg1: input mode. [Mantual,Timer,GPIO]
arg2: Capture interval for Timer mode (float)
arg3: Numbers of capturing for Timer mode (int)
'''


def GetArgs_Mode(argv):
    if len(argv) > 1: return argv[1]
    raise IOError('input mode not found')
def GetArgs_GetCaptureInterval(argv):
    if len(argv) > 1: return float(argv[2])
    return -1.
def GetArgs_NumberImagesCaptured(argv):
    if len(argv) > 2: return int(argv[3])
    print('No arg2 input!!! This code only capture 10 figures')
    return 10

def ShowTimer(t,mesg):
    print('time : %s --- %s' % (time.strftime("%H:%M:%S", time.localtime(t)),mesg))
class formatted_idx:
    def __init__(self):
        self.idx = 0
    def __str__(self):
        return '%04d' % self.idx
    def PlusOne(self):
        self.idx += 1

class StatusCollecter:
    _CODE_GOOOOOOOOOOOD =  0 #  normal
    _CODE_INVALID_INPUT = -1 #  wrong input got
    _CODE_ERR_DELIEVERY = -2 #  outside error

    def __init__(self, raisingERROR: str = "" ):
        self.wronginterval = 0
        if raisingERROR == "": self.stat = StatusCollecter._CODE_GOOOOOOOOOOOD
        self.errorMesg = raisingERROR
        self.stat = StatusCollecter._CODE_ERR_DELIEVERY

    def othererror(self):
        if self.stat == StatusCollecter._CODE_ERR_DELIEVERY: return self.errorMesg
        return None

    def SetWarning(self) -> None:
        if self.othererror(): return
        self.stat = StatusCollecter._CODE_INVALID_INPUT
        self.wronginterval = 5 # message keeps 10 intervals
    def Succeed(self) -> None:
        if self.othererror(): return
        self.stat = StatusCollecter._CODE_GOOOOOOOOOOOD
    def CheckStatus(self) -> None:
        if self.othererror(): return
        if self.stat != StatusCollecter._CODE_INVALID_INPUT: return

        self.wronginterval -= 1
        if self.wronginterval < 0:
            self.stat = StatusCollecter._CODE_GOOOOOOOOOOOD # reset
    def ShowStatus(self, idx_ : formatted_idx) -> str:
        if self.stat == StatusCollecter._CODE_ERR_DELIEVERY: return self.errorMesg
        if self.stat == StatusCollecter._CODE_INVALID_INPUT: return "Wrong input"
        if self.stat == StatusCollecter._CODE_GOOOOOOOOOOOD: return "Capturing: img_%s.jpg" % idx_
        return "no stat shown"


def ManualCapture(vid, runstat):
    imgidx = formatted_idx()
    while(True):

        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        usageHelp = '''---- Usage ----\n'''
        usageHelp+= '''    * Capture: "space bar"\n'''
        usageHelp+= '''    * Quit: "esc"\n'''
        usageHelp+= '''    Status %s'''%runstat.ShowStatus(imgidx)

        add_helper_mesg_to(frame,usageHelp)


        # Display the resulting frame
        try:
            cv2.imshow('frame', frame)
        except: # AssertionError as msg:
            print('""""error found """" : %s\n\n' % msg)
            print('the reason might be no camera found')
            exit(1)


        # 'space' : capture
        # 'esc' : quit program
        # the 'esc' button is set as the
        # quitting button you may use any
        # desired button of your choice
        waitkey = cv2.waitKey(1)
        if   waitkey == 27: # esc key
            break
        #elif runstat.
        elif waitkey == 32: # space key
            print('new file created: img_%s.png'%imgidx)
            cv2.imwrite('%s/img_%s.jpg'%(outDir,imgidx), frame)
            imgidx.PlusOne()
            runstat.Succeed()
        elif waitkey == -1: # nothing
            time.sleep(0.1)
            runstat.CheckStatus()

        else: # other key input. Will show wrong input
            runstat.SetWarning()
def auto_helper_message(mesgs):
    ''' Generate message with format

    ---- Autimatically Capturing ----
        str1
        str2
        str3


        Args: str list

        Return: str
    '''
    out = '---- Autimatically Capturing ----\n'
    return out + '    '.join(mesg+'\n' for mesg in mesgs)
def AutomaticMode(vid, runstat, captureDURATION=3, maxNum_=100):
    imgidx = formatted_idx()
    ### 0  : init stat
    ### >0 : capturing
    ### <0 : paused
    started=0
    captured=False

    usageHelperInit = auto_helper_message(['Press SPACE to start capturing'])
    usageHelperStop = auto_helper_message(['Press SPACE to continue capturing','ESC to escape'])
    usageHelperNorm = auto_helper_message(['Status {thestatus}','ESC to escape'])

    while(maxNum_):
        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        usageHelp = ''
        if started == 0 and not captured:
            usageHelp = usageHelperInit
        if started < 0:
            usageHelp = usageHelperStop
        if started > 0:
            usageHelp = usageHelperNorm.format(thestatus=runstat.ShowStatus(imgidx))

        add_helper_mesg_to(frame,usageHelp)

        # Display the resulting frame
        try:
            cv2.imshow('frame', frame)
        except: # AssertionError as msg:
            print('""""error found """" : %s\n\n' % msg)
            print('the reason might be no camera found')
            exit(1)


        waitkey = cv2.waitKey(1)
        # 'space' : capture start
        if waitkey == 32: # space key
            if started == 0:
                started=1
                startTimer=time.time()
                ShowTimer(startTimer,"start capturing")
            else:
                started *= -1
                # reset timer to capture after pause
                captured=False
                startTimer=time.time()
        if   waitkey == 27: # esc key
            break

        if started > 0:
            currentTimer = time.time()
            if not captured: # capture image now
            #if not captured and int(time.time()-startTimer) % captureDURATION ==0:
                ShowTimer(currentTimer, "capturing picture")
                # take picture
                print('new file created: img_%s.png'%imgidx)
                cv2.imwrite('%s/img_%s.jpg'%(outDir,imgidx), frame)
                imgidx.PlusOne()
                runstat.Succeed()
                if imgidx.idx > maxNum_: return
                captured=True

            if captured:
                if (currentTimer-startTimer) > captureDURATION:
                    startTimer = currentTimer
                    captured = False
                    ShowTimer(currentTimer, "+%f sec : reset capture status"%captureDURATION)

        #time.sleep(0.1)

# ''' GPIO section '''
# #GPIO.setmode(GPIO.BCM) # Use BCM pin numbering
# GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
# pin=11 #physical pin number
# GPIO.setup(pin, GPIO.IN) # Set pin as input
# pin_value = GPIO.input(pin) # read GPIO value # asdf how to decide HIGH and LOW?
# ''' GPIO section end '''
def GPIOMode(vid, runstat):
    '''
    GPIO High : capture photo
    GPIO Low  : wait program
    Continuous GPIO High : stop program
    '''
    imgidx = formatted_idx()
    ### 0  : init stat
    ### >0 : capturing
    ### <0 : paused
    started=0
    captured=False

    usageHelperInit = auto_helper_message(['Press START to start capturing'])
    usageHelperStop = auto_helper_message(['Press START to continue capturing','ESC to escape'])
    usageHelperNorm = auto_helper_message(['Status {thestatus}','ESC to escape'])

    #GPIO.setmode(GPIO.BCM) # Use BCM pin numbering
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    RPiPin=11 #physical pin number
    GPIO.setup(RPiPin, GPIO.IN) # Set pin as input

    status2=0 # record previous 2 status
    status1=0 # record previous 1 status
    while True:
        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        usageHelp = ''
        if started == 0 and not captured:
            usageHelp = usageHelperInit
        if started < 0:
            usageHelp = usageHelperStop
        if started > 0:
            usageHelp = usageHelperNorm.format(thestatus=runstat.ShowStatus(imgidx))

        add_helper_mesg_to(frame,usageHelp)

        # Display the resulting frame
        try:
            cv2.imshow('frame', frame)
        except: # AssertionError as msg:
            print('""""error found """" : %s\n\n' % msg)
            print('the reason might be no camera found')
            exit(1)


        pin_value = GPIO.input(RPiPin) # read GPIO value # 0: low 1:high

        currentTimer = time.time()
        waitkey = cv2.waitKey(1)
        if   waitkey == 27: # esc key
            # break program by keyboard
            ShowTimer(currentTimer, "program exited by user")
            break
        if pin_value == 1 and status1 == 1 and status2 == 1:
            # break program by external trigger
            ShowTimer(currentTimer, "program done")
            break

        if pin_value == 1 and status1 == 0:
            # capture image
            ShowTimer(currentTimer, "%s/Auto_GPIOCapture_%s.jpg captured"%(outDir,imgidx))
            cv2.imwrite('%s/img_%s.jpg'%(outDir,imgidx), frame)
            imgidx.PlusOne()
            runstat.Succeed()
        # status delivery for break program
        status2 = status1
        status1 = pin_value

        #time.sleep(0.1)


def add_helper_mesg_to(frame, usageHelp: str) -> None:
    # put text into video
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontsize = 0.6
    lineheight = 25
    for idxLine,line in enumerate(usageHelp.split('\n'),1):
        cv2.putText(frame,
        line, (0,0+idxLine*lineheight),
        font,fontsize,(204,153,255),2,cv2.LINE_4)


if __name__ == "__main__":
    import os
    import sys
    runmode = GetArgs_Mode(sys.argv)
    capInterval = GetArgs_GetCaptureInterval(sys.argv)
    numImgCaptured = GetArgs_NumberImagesCaptured(sys.argv)

    currentTime = time.time()
    outDir = time.strftime("AutoCapture_%Y-%m-%d_%H:%M", time.localtime(currentTime))
    recordPathChecking = '' if not os.path.exists(outDir) else 'Error! folder "%s" exists!! Delete it first'%outDir
    if recordPathChecking == '': os.mkdir(outDir)

    # define a video capture object
    #vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    vid = cv2.VideoCapture('/dev/video0')

    runstat = StatusCollecter(recordPathChecking)

    if runmode == 'Manual':
        ManualCapture(vid, runstat)
    if runmode == 'Timer':
        AutomaticMode(vid, runstat, capInterval, numImgCaptured)
    if runmode == 'GPIO':
        GPIOMode(vid, runstat)

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
