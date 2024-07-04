#!/usr/bin/env python3
import time
import threading
#import frag_photo_capture_windows
import SerialDeviceMgr.macAPI as serialDevAPI
#import PhotoCapturingAPI.macAPI as photoCaptureAPI
import PhotoCapturingAPI.windowsAPI as photoCaptureAPI
import yaml


SLEEP_BKG = 1.0 # second
MOVING_DELAY = 0.1 # this will be updated in yaml file
CAPTUR_DELAY = 2.0 # this will be updated in yaml file
def BUG(mesg):
    bug_mode = False
    if bug_mode:
        print(f'[BUG] {mesg}')

### test func {{{
def jobComponent_minigantry_next_point( delayTIMER ) -> int:
    '''
    job status is returned.
    '''
    raise NotImplementedError('This function is required to be overwritten before use')
    SecondaryLog('moving position to next point')
    time.sleep(delayTIMER)
    return 1
def jobComponent_take_photo(delayTIMER) -> int:
    '''
    job status is returned.
    '''
    #raise NotImplementedError('This function is required to be overwritten before use')
    SecondaryLog('capturing photon...')
    time.sleep(delayTIMER)
    return 1
### test func end }}}


def PrimaryLog(mesg):
    print(f'[PrimaryLog] {mesg}')
def SecondaryLog(mesg):
    print(f'[SecondaryLog] {mesg}')
def SetLog(primaryLOGfunc, secondaryLOGfunc):
    BUG('Update log functions at background process')
    serialDevAPI.SetLog(primaryLOGfunc,secondaryLOGfunc)
    photoCaptureAPI.SetLog(primaryLOGfunc,secondaryLOGfunc)
    global PrimaryLog, SecondaryLog
    PrimaryLog = primaryLOGfunc
    SecondaryLog = secondaryLOGfunc
    
class ProgramStatus:
    def __init__(self):
        self.activatingFlag = threading.Event()
        self.programIsAlive = threading.Event()
        self.programIsAlive.set()



def run_job(progSTAT:ProgramStatus,):

    #totIDX = progSTAT.totIdx
    programACTIVATING = progSTAT.programIsAlive
    keepCAPTURING = progSTAT.activatingFlag

    capIdx = 0
    while programACTIVATING.is_set():
        if keepCAPTURING.is_set():
            capIdx += 1
            PrimaryLog(f'Capturing image {capIdx}') # capIdx from 1 ~ N
            job_stat1 = jobComponent_minigantry_next_point(MOVING_DELAY)
            job_stat2 = jobComponent_take_photo(CAPTUR_DELAY)

            if   job_stat1 == 0:
                PrimaryLog('Job finished from Mini gantry')
                programACTIVATING.clear()
            elif job_stat2 == 0:
                PrimaryLog('Job finished from photo taking')
                programACTIVATING.clear()
        else:
            PrimaryLog(f'Capturing image {capIdx} is Paused')
            SecondaryLog('')
            time.sleep(SLEEP_BKG)
    # the GUI is no longer activating, so not to show anything at the end.
    PrimaryLog('program ended')
    SecondaryLog(f'{capIdx} photo captured')
    print('[JobFinished] background job is stopped')





def bkg_run_job(programSTATUS):
    t = threading.Thread(target=run_job, args=(programSTATUS,))
    t.start()
    return t





def testfunc_direct_run_func(programSTATUS):
    # need to be updated
    programSTATUS = ProgramStatus()
    programSTATUS.activatingFlag.set()

    run_job(programSTATUS)
    exit()

def testfunc_bkg_run_func(programSTATUS):
    # need to be updated
    def primary_message(mesg):
        print(f'[primary] {mesg}')
    def secondary_message(mesg):
        print(f'[secondary] {mesg}')
    PrimaryLog = primary_message
    SecondaryLog = secondary_message

    t = bkg_run_job(programSTATUS)

    time.sleep(4)
    programSTATUS.activatingFlag.set()

    t.join()
    exit()

class API:
    def __init__(self, yamlFILE):
        self.code_blocker = 0
        with open(yamlFILE,'r') as fIN:
            self.configs = yaml.safe_load(fIN)
        if self.configs['operation_system'] == 'test':
            pass # ignore testing
        elif serialDevAPI.OPERATION_SYSTEM != self.configs['operation_system']:
            PrimaryLog('Wrong OS')
            SecondaryLog(f'Loaded YAML file is suitable for {self.configs["operation_system"]} but code is for {serialDevAPI.OPERATION_SYSTEM}')
            self.code_blocker = 1 # forbidden by OS error
            return
        elif photoCaptureAPI.OPERATION_SYSTEM != self.configs['operation_system']:
            PrimaryLog('Wrong OS')
            SecondaryLog(f'Loaded YAML file is suitable for {self.configs["operation_system"]} but code is for {serialDevAPI.OPERATION_SYSTEM}')
            self.code_blocker = 1 # forbidden by OS error
            return

        self.components_minigantry_movement = serialDevAPI.APIfactory(self.configs['SerialDeviceMgr'])
        self.components_photo_capture = photoCaptureAPI.APIfactory(self.configs['PhotoCapturingAPI'])

        global CAPTUR_DELAY, MOVING_DELAY
        MOVING_DELAY = self.configs['Moving Delay']
        CAPTUR_DELAY = self.configs['Capturing Delay']


    def set(self, **xargs):
        if self.code_blocker != 0: return
        self.components_minigantry_movement.set(**xargs)
        self.components_photo_capture.set(**xargs)
        try:
            global CAPTUR_DELAY, MOVING_DELAY
            MOVING_DELAY = float(xargs['Moving Delay'])
            CAPTUR_DELAY = float(xargs['Capturing Delay']) 
        except ValueError as e:
            BUG(f'[ErrorFromVariableSet] {e}')
            PrimaryLog('Invalid value')
            SecondaryLog('Input number')
        BUG(f'[DelayUpdated] moving delay {MOVING_DELAY} and capturing delay {CAPTUR_DELAY}')


    def list_setting(self) -> list:
        if self.code_blocker != 0: return
        o = []
        BUG(self.components_minigantry_movement.list_setting())
        o.extend(self.components_minigantry_movement.list_setting())
        o.extend(self.components_photo_capture.list_setting())
        o.append( {'name': 'Moving Delay'   , 'type': 'text', 'default': MOVING_DELAY} )
        o.append( {'name': 'Capturing Delay', 'type': 'text', 'default': CAPTUR_DELAY} )
        return o
    def dummy_run(self):
        if self.code_blocker != 0: return
        def dummy_minigantry_next_point(delayTIMER) -> int:
            SecondaryLog('Sending command to Mini gantry')
            ''' testing section '''
            run_status = self.components_minigantry_movement.run()
            BUG('Hiiiii this is dummy mini gantry next point')
            #run_status = self.__get_counter()
            ''' testing section '''

            time.sleep(delayTIMER)
            if run_status == 0:
                SecondaryLog('No further signal from mini gantry')
            else:
                SecondaryLog('Mini gantry finished the movement')
            BUG(f'delaying moving {delayTIMER}')
            return run_status
        global jobComponent_minigantry_next_point # modify the function directly
        jobComponent_minigantry_next_point = dummy_minigantry_next_point


        def dummy_take_photo(delayTIMER) -> int:
            SecondaryLog('Taking photo...')
            ''' testing section '''
            run_status = self.components_photo_capture.run()
            BUG('Hiiiii this is dummy photo capturing procedure')
            ''' testing section '''

            time.sleep(delayTIMER)
            if run_status == 0:
                SecondaryLog('Something Stucked photo capturing')
            else:
                SecondaryLog('Photo captured')
            BUG(f'delaying photo taking {delayTIMER}')
            return run_status
        global jobComponent_take_photo # modify the function directly
        jobComponent_take_photo = dummy_take_photo


        #def A(mesg):
        #    print(f'[AAAAA] {mesg}')
        #def a(mesg):
        #    print(f'[aaaaa] {mesg}')
        #SetLog(A,a)

        self.programStatus = ProgramStatus()
        self.job_thread = bkg_run_job(self.programStatus)
    def run(self):
        if self.code_blocker != 0: return
        self.dummy_run()
        # def realFunc_minigantry_next_point(delayTIMER) -> int:
        #     SecondaryLog('Sending command to Mini gantry')
        #     ''' testing section '''
        #     #run_status = self.components_minigantry_movement.run()
        #     run_status = 10
        #     ''' testing section '''

        #     time.sleep(delayTIMER)
        #     if run_status == 0:
        #         SecondaryLog('No further signal from mini gantry')
        #     else:
        #         SecondaryLog('Mini gantry finished the movement')
        #     return run_status
        # global jobComponent_minigantry_next_point # modify the function directly
        # jobComponent_minigantry_next_point = realFunc_minigantry_next_point

        # def realFunc_take_photo(delayTIMER) -> int:
        #     SecondaryLog('Taking photo...')
        #     ''' testing section '''
        #     #run_status = self.components_minigantry_movement.run()
        #     run_status = 1
        #     ''' testing section '''

        #     time.sleep(delayTIMER)
        #     if run_status == 0:
        #         SecondaryLog('Something Stucked photo capturing')
        #     else:
        #         SecondaryLog('Photo captured')
        #     PrimaryLog(f'delaying photo taking {delayTIMER}')
        #     return run_status
        # global jobComponent_take_photo # modify the function directly
        # jobComponent_take_photo = realFunc_take_photo

        # self.programStatus = ProgramStatus()
        # self.job_thread = bkg_run_job(self.programStatus)
        

    def start(self): self.programStatus.activatingFlag.set()
    def pause(self): self.programStatus.activatingFlag.clear()
        

    
        


def testfunc_useAPI():
    #bkgrun_api = API('data/bkg_process_macOS.yaml')
    bkgrun_api = API('data/bkg_process.yaml')
    set_values = {}
    for l in bkgrun_api.list_setting():
        n = l['name']
        v = 0
        if 'options' in l:
            v = l['options'][0]
        if 'default' in l:
            v = l['default']

        set_values[n] = v
        

    bkgrun_api.set(**set_values)

    bkgrun_api.run()
    time.sleep(3)
    bkgrun_api.start()


    bkgrun_api.job_thread.join()
    exit()

if __name__ == "__main__":
    testfunc_useAPI()

    #programStatus = ProgramStatus()
    #testfunc_bkg_run_func(programStatus)

