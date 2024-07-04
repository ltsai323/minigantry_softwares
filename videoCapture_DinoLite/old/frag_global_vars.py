#!/usr/bin/env python3
import threading

class ProgramStatus:
    def __init__(self, totIDX, logfuncSTAT=lambda mesg:print(mesg), logfuncACTION=lambda mesg:print(mesg)):
        self.activatingFlag = threading.Event()
        self.programIsAlive = threading.Event()
        self.programIsAlive.set()

        self.message = 'Program Initializing'
        self.actlogFunc = logfuncACTION
        self.statusFunc = logfuncSTAT
        self.actionMesg = 'moving position to mini gantry'
        self.statusMesg = 'Capturing 0 / 100 mesg'
        self.totIdx = totIDX
    def SetMesg(self, newMESG):
        self.message = newMESG
    def SetStatus(self, newMESG):
        self.statusMesg = newMESG
        self.statusFunc(newMESG)
    def SetAction(self, newMESG):
        self.actionMesg = newMESG
        self.actlogFunc(newMESG)
        


if __name__ == "__main__":
    programStat = ProgramStatus(30)
    print(f'program is alived ? {programStat.programIsAlive.is_set()}')
    print(f'program is activating ? {programStat.activatingFlag.is_set()}')
    print(f'Message : {programStat.message}')
    print(f'Capturing {programStat.capIdx} / {programStat.totIdx}')
