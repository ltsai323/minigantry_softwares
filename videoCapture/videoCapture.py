# import the opencv library
import cv2

class FormattedIdx:
    def __init__(self):
        self.idx = 0
    def __str__(self):
        return '%04d' % self.idx
    def PlusOne(self):
        self.idx += 1

class StatusCollecter:
    # stat =  0 : normal
    # stat = -1 : wrong input got
    # stat = -2 : outside error
    _CODE_GOOOOOOOOOOOD =  0
    _CODE_INVALID_INPUT = -1
    _CODE_ERR_DELIEVERY = -2

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
        return ""
        

def AddHelperMesgTo(frame, runstat: StatusCollecter, imgidx: FormattedIdx) -> None:
    # put text into video
    usageHelp = '''---- Usage ----
    * Capture: "space bar"
    * Quit: "esc"
    Status %s'''%runstat.ShowStatus(imgidx)

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontsize = 0.6
    lineheight = 25
    for idxLine,line in enumerate(usageHelp.split('\n'),1):
        cv2.putText(frame,
        line, (0,0+idxLine*lineheight),
        font,fontsize,(204,153,255),2,cv2.LINE_4)

if __name__ == "__main__":
    
    import os
    tmpdir = 'tmpdir'
    recordPathChecking = '' if not os.path.exists(tmpdir) else 'Error! tmp folder "%s" exists!! Delete it first'%tmpdir
    if recordPathChecking == '': os.mkdir(tmpdir)
    
    # define a video capture object
    vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    import time
    imgidx = FormattedIdx()
    runstat = StatusCollecter(recordPathChecking)
    while(True):
        
        # Capture the video frame
        # by frame
        ret, frame = vid.read()
    
        AddHelperMesgTo(frame,runstat, imgidx)
    
    
        # Display the resulting frame
        try:
            cv2.imshow('frame', frame)
        except: # AssertionError as msg:
            #print('""""error found """" : %s' % msg)
            print('the reason might be no camera found')
            os.system('pause')
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
            cv2.imwrite('%s/img_%s.jpg'%(tmpdir,imgidx), frame)
            imgidx.PlusOne()
            runstat.Succeed()
        elif waitkey == -1: # nothing
            time.sleep(0.1)
            runstat.CheckStatus()
            
        else: # other key input. Will show wrong input
            runstat.SetWarning()
    
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()