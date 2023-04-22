#!/usr/bin/env python3
# import the opencv library
import cv2
import datetime

def GetArgs_GetCaptureInterval(argv):
    if len(argv) > 1: return int(argv[1])
    return -1
def GetArgs_NumberImagesCaptured(argv):
    if len(argv) > 2: return int(argv[2])
    print('No arg2 input!!! This code only capture 10 figures')
    return 10

def ShowTimer(t,mesg):
    print('time : %s --- %s' % (time.strftime("%H:%M:%S", time.localtime(t)),mesg))
class FormattedIdx:
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
    def ShowStatus(self, idx_ : FormattedIdx) -> str:
        if self.stat == StatusCollecter._CODE_ERR_DELIEVERY: return self.errorMesg
        if self.stat == StatusCollecter._CODE_INVALID_INPUT: return "Wrong input"
        if self.stat == StatusCollecter._CODE_GOOOOOOOOOOOD: return "Capturing: img_%s.jpg" % idx_
        return "no stat shown"


def ManualCapture(vid, runstat):
    imgidx = FormattedIdx()
    while(True):

        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        usageHelp = '''---- Usage ----\n'''
        usageHelp+= '''    * Capture: "space bar"\n'''
        usageHelp+= '''    * Quit: "esc"\n'''
        usageHelp+= '''    Status %s'''%runstat.ShowStatus(imgidx)

        AddHelperMesgTo_(frame,usageHelp)


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
def AutoHelperMessage(mesgs):
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
    imgidx = FormattedIdx()
    ### 0  : init stat
    ### >0 : capturing
    ### <0 : paused
    started=0
    captured=False

    usageHelperInit = AutoHelperMessage(['Press "space" to start capturing'])
    usageHelperStop = AutoHelperMessage(['Press "space" to continue capturing'])
    usageHelperNorm = AutoHelperMessage(['Status {thestatus}','ESC to escape'])

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

        #usageHelp = '''---- Automatically Capturing ----\n'''
        #if started == 0 and not captured:
        #    usageHelp+= '''    Press "space" to start capturing \n'''
        #if started < 0:
        #    usageHelp+= '''    Press "space" to continue capturing \n'''
        #if started > 0:
        #    usageHelp+= '''    Status %s'''%runstat.ShowStatus(imgidx)
        AddHelperMesgTo_(frame,usageHelp)

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
                starttimer=time.time()
                ShowTimer(starttimer,"start capturing")
            else:
                started *= -1
                # reset timer to capture after pause
                captured=False
                starttimer=time.time()
        if   waitkey == 27: # esc key
            break

        if started > 0:
            if not captured and int(time.time()-starttimer) % captureDURATION ==0:
                ShowTimer(time.time(), "capturing picture")
                # take picture
                print('new file created: img_%s.png'%imgidx)
                cv2.imwrite('%s/img_%s.jpg'%(outDir,imgidx), frame)
                imgidx.PlusOne()
                runstat.Succeed()
                if imgidx.idx > maxNum_: return
                captured=True

            if captured:
                if int(time.time()-starttimer) % captureDURATION !=0:
                    captured=False
                    ShowTimer(time.time(), "+1 sec : reset capture status")

        time.sleep(0.1)


def AddHelperMesgTo_(frame, usageHelp: str) -> None:
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
    capInterval = GetArgs_GetCaptureInterval(sys.argv)
    numImgCaptured = GetArgs_NumberImagesCaptured(sys.argv)

    currentTime = datetime.datetime.now()
    outDir = currentTime.strftime("AutoCapture_%Y-%m-%d_%H-%M")
    recordPathChecking = '' if not os.path.exists(outDir) else 'Error! tmp folder "%s" exists!! Delete it first'%outDir
    if recordPathChecking == '': os.mkdir(outDir)

    # define a video capture object
    #vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    vid = cv2.VideoCapture('/dev/video0')

    import time
    runstat = StatusCollecter(recordPathChecking)

    if capInterval > 0:
        AutomaticMode(vid, runstat, capInterval, numImgCaptured)
    else:
        ManualCapture(vid, runstat)

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
